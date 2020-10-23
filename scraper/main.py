import logging
import sys
from os.path import dirname

from decouple import AutoConfig
from mongoengine import connect

sys.path.insert(0, dirname(__file__))

from scraper import Scraper

conn = connect('upa', host='mongo', username='scraper', password='scraper')
config = AutoConfig()

logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

scraper = Scraper(
    config=config,
    connection=conn
)

scraper.run()
