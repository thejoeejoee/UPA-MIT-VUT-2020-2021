import argparse
import logging
import sys
from os.path import dirname

from decouple import AutoConfig
from mongoengine import connect


def main():
    sys.path.insert(0, dirname(__file__))
    from scraper import Scraper

    conn = connect('upa', host='mongo', username='scraper', password='scraper')
    config = AutoConfig()

    logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

    scraper = Scraper(
        config=config,
        connection=conn
    )

    parser = argparse.ArgumentParser(description='Scrape data from FTP/local directory and store them in mongo.')

    parser.add_argument('action', choices=('ftp', 'local-dir'))

    args = parser.parse_args()

    if args.action == 'ftp':
        scraper.run_from_ftp()
    elif args.action == 'local-dir':
        scraper.run_from_local_dir()


exit(main())
