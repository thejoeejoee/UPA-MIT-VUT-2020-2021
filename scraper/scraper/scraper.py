import os
from datetime import datetime
from ftplib import FTP
from os import makedirs, stat

import xmltodict
from dateutil import parser
from decouple import AutoConfig
from pymongo import MongoClient

from . import logger
from .models import Station


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

        # TODO: find best way to unwind measurements
        station = Station()
        station.data = data

        station.save()
