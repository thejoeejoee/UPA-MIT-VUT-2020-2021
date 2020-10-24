import os
from datetime import datetime
from ftplib import FTP
from os import makedirs, stat
from typing import Optional

import xmltodict
from dateutil import parser
from decouple import AutoConfig
from pymongo import MongoClient

from . import logger
from .conf import MEASUREMENT_ATTRS_MAPPING, MEASUREMENT_ATTRS_TO_SKIP
from .models import Station, Measurement


class Scraper:
    """
    Class managing scraping data from given host to given Mongo instance defined by connection.
    """

    def __init__(
            self,
            config: AutoConfig,
            connection: MongoClient
    ):
        self._config = config
        self._connection = connection

    def run(self):
        local_storage_dir = self._config('LOCAL_STORAGE_DIR')

        scraped = self._scrape()

        makedirs(local_storage_dir, exist_ok=True)

        for f in scraped:
            with open(os.path.join(local_storage_dir, f), 'r') as fd:
                self._store_data(file_content=fd.read())

    def _scrape(self):
        host = self._config('FTP_HOST')
        files_to_scrape = set(self._config('FILES_TO_SCRAPE').split())
        dir_to_scrape = self._config('FTP_DIR')
        local_storage_dir = self._config('LOCAL_STORAGE_DIR')

        logger.debug('Logging to FTP %s in progress.', host)

        with FTP(host=host, ) as ftp:
            ftp.login()
            ftp.cwd(dir_to_scrape)

            scraped_files = set()
            ftp.retrlines('NLST', scraped_files.add)

            found_to_scrape = scraped_files & files_to_scrape

            logger.debug('Found %s files to scrape: %s.', len(files_to_scrape), ','.join(found_to_scrape))

            for i, to_scrape in enumerate(found_to_scrape, start=1):
                local_file_pth = os.path.join(local_storage_dir, to_scrape)

                last_modified_remote = self.remote_file_last_modified(ftp, to_scrape)
                last_modified_local = self._local_file_last_modified(local_file_pth)

                if last_modified_remote and last_modified_local and last_modified_local > last_modified_remote:
                    logger.debug(
                        'File %s: %s skipped (last modified difference %s).',
                        i, to_scrape, last_modified_local - last_modified_remote
                    )
                    continue

                with open(local_file_pth, 'wb') as local_fp:
                    ftp.retrbinary(f'RETR {to_scrape}', local_fp.write)

                logger.debug('File %s: %s has been scraped.', i, to_scrape)
            return found_to_scrape

    @staticmethod
    def remote_file_last_modified(ftp: FTP, file_name: str):
        modified = ftp.voidcmd(f'MDTM {file_name}')[4:].strip()

        try:
            return parser.parse(modified)
        except (ValueError, OverflowError):
            return None

    @staticmethod
    def _local_file_last_modified(file_name: str):
        try:
            stats = stat(file_name)
        except FileNotFoundError:
            return None

        return datetime.fromtimestamp(stats.st_mtime)

    def _store_data(self, file_content: str):
        data = xmltodict.parse(file_content)

        stations = data.get("product").get("observations").get("station")
        for station_data in stations:
            wmo_id = int(station_data.get("@wmo-id"))

            # checking existence of station
            station = self._get_or_create_station(station_data, wmo_id)

            logger.debug('Loading measurement from %s: %s.', wmo_id, station.station_name)

            measurement = Measurement()
            measurement.station = station.to_dbref()
            period = station_data.get("period")
            measurement.time_period = period.get("@time-utc")

            elements = period.get("level").get("element")
            if elements is None:
                break

            for element in elements:
                if type(element) == str:  # should probably check if element is OrderedDict
                    logger.warning('Skipped text element %s.', element)
                    break

                attr_type = (element.get("@type") or '').replace('-', '_')

                if attr_type in MEASUREMENT_ATTRS_TO_SKIP:
                    continue

                data_type: Optional[callable] = MEASUREMENT_ATTRS_MAPPING.get(attr_type)
                if not data_type:
                    logger.warning('Unknown attribute %s.', attr_type)
                    continue

                setattr(
                    measurement,
                    attr_type,
                    data_type(element)
                )

            measurement.save()

    @staticmethod
    def _get_or_create_station(data, wmo_id):
        fetched_station = Station.objects(wmo_id=wmo_id)
        if not fetched_station:
            station = Station()
            station.wmo_id = wmo_id
            station.location = data.get("@tz")
            station.station_name = data.get("@stn-name")
            station.station_height = float(data.get("@stn-height"))
            station.latitude = float(data.get("@lat"))
            station.longitude = float(data.get("@lon"))
            station.save()
        else:
            station = fetched_station.first()
        return station
