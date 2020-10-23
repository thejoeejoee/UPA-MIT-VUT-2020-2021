import os
from ftplib import FTP

import xmltodict
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

        scraped = self._scrape(skip_download=True)

        for f in scraped:
            with open(os.path.join(local_storage_dir, f), 'r') as fd:
                self._store_data(file_content=fd.read())

    def _scrape(self, skip_download=False):
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

            if skip_download:
                return found_to_scrape

            # TODO: scrape only modified files (smth like ftp.stat?)
            for i, to_scrape in enumerate(found_to_scrape, start=1):
                with open(os.path.join(local_storage_dir, to_scrape), 'wb') as local_fp:
                    ftp.retrbinary(f'RETR {to_scrape}', local_fp.write)

                logger.debug('File %s: %s has been scraped.', i, to_scrape)
            return found_to_scrape

    def _store_data(self, file_content: str):
        data = xmltodict.parse(file_content)

        # TODO: find best way to unwind measurements
        station = Station()
        station.data = data

        station.save()
