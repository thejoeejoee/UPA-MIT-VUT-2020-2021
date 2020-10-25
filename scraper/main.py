import logging
import sys
from datetime import timedelta, datetime
from os.path import dirname
from time import sleep

from decouple import AutoConfig
from mongoengine import connect

sys.path.insert(0, dirname(__file__))

from scraper import Scraper, logger

conn = connect('upa', host='mongo', username='scraper', password='scraper')
config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

scraper = Scraper(
    config=config,
    connection=conn
)

while True:
    scraper.run()
    logger.info('Waiting till %s to rescrape.', (datetime.now() + timedelta(minutes=10)))
    sleep(10 * 60)
