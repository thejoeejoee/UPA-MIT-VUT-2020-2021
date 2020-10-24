import os
from datetime import datetime
from ftplib import FTP
from os import makedirs, stat

import xmltodict
from dateutil import parser
from decouple import AutoConfig
from pymongo import MongoClient

from . import logger
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
            fetched_station = Station.objects(wmo_id=wmo_id)  # returns QuerySet
            if not fetched_station:
                station = Station()
                station.wmo_id = wmo_id
                station.location = station_data.get("@tz")
                station.station_name = station_data.get("@stn-name")
                station.station_height = float(station_data.get("@stn-height"))
                station.latitude = float(station_data.get("@lat"))
                station.longitude = float(station_data.get("@lon"))
                station.save()
            else:
                station = fetched_station.first()

            measurement = Measurement()
            measurement.station = station.to_dbref()
            period = station_data.get("period")
            measurement.time_period = period.get("@time-utc")

            elements = period.get("level").get("element")
            if elements is None:
                break
            for element in elements:
                if type(element) == str:  # should probably check if element is OrderedDict
                    break
                element_type = element.get("@type")
                element_value = element.get("#text")
                if element_type == "time_period":
                    measurement.time_period = element_value
                elif element_type == "apparent_temp":
                    measurement.apparent_temp = float(element_value)
                elif element_type == "cloud":
                    measurement.cloud = element_value
                elif element_type == "cloud_oktas":
                    measurement.cloud_oktas = int(element_value)
                elif element_type == "cloud_type_id":
                    measurement.cloud_type_id = int(element_value)
                elif element_type == "delta_t":
                    measurement.delta_t = float(element_value)
                elif element_type == "air_temperature":
                    measurement.air_temperature = float(element_value)
                elif element_type == "dew_point":
                    measurement.dew_point = float(element_value)
                elif element_type == "pres":
                    measurement.pres = float(element_value)
                elif element_type == "msl_pres":
                    measurement.msl_pres = float(element_value)
                elif element_type == "qnh_pres":
                    measurement.qnh_pres = float(element_value)
                elif element_type == "rain_hour":
                    measurement.rain_hour = float(element_value)
                elif element_type == "rain_ten":
                    measurement.rain_ten = float(element_value)
                elif element_type == "rel_humidity":
                    measurement.rel_humidity = int(element_value)
                elif element_type == "vis_km":
                    measurement.vis_km = float(element_value)
                elif element_type == "weather":
                    measurement.weather = element_value
                elif element_type == "wind_dir":
                    measurement.wind_dir = element_value
                elif element_type == "wind_dir_deg":
                    measurement.wind_dir_deg = int(element_value)
                elif element_type == "wind_spd_kmh":
                    measurement.wind_spd_kmh = int(element_value)
                elif element_type == "wind_spd":
                    measurement.wind_spd = int(element_value)
                elif element_type == "gust_kmh":
                    measurement.gust_kmh = int(element_value)
                elif element_type == "wind_gust_spd":
                    measurement.wind_gust_spd = int(element_value)
                elif element_type == "rainfall":
                    measurement.rainfall = element
                elif element_type == "rainfall_24hr":
                    measurement.rainfall_24hr = element
                elif element_type == "maximum_air_temperature":
                    measurement.maximum_air_temperature = element
                elif element_type == "minimum_air_temperature":
                    measurement.minimum_air_temperature = element
                elif element_type == "maximum_gust_spd":
                    measurement.maximum_gust_spd = element
                elif element_type == "maximum_gust_kmh":
                    measurement.maximum_gust_kmh = element
                elif element_type == "maximum_gust_dir":
                    measurement.maximum_gust_dir = element
            measurement.save()
