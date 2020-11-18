import argparse
import logging
import sys
from os.path import dirname

from decouple import AutoConfig
from mongoengine import connect


def main():
    sys.path.insert(0, dirname(__file__))

    connect('upa', host='mongo', username='computer', password='computer')
    config = AutoConfig()

    logging.basicConfig(level=config('LOG_LEVEL', cast=int, default=logging.INFO))

    parser = argparse.ArgumentParser(description='...')

    args = parser.parse_args()

    from computer import Computer
    computer = Computer()
    computer.run()


exit(main())
