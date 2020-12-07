from django.utils import dateparse

from models import MeasurementDocument
from models.models import Temperature, Rainfall
from . import logger
from .syncer import Syncer


class Computer(object):

    def run(self):
        Syncer.sync_stations()

        temperature_pipeline = [
            {
                "$match": {
                    "air_temperature": {"$ne": None},
                },
            },
            {
                "$lookup":
                    {
                        "from": 'station',
                        "localField": 'station',
                        "foreignField": '_id',
                        "as": 'station',
                    },
            },
            {
                "$unwind": {"path": '$station'},
            },
            {
                "$project": {
                    "station": "$station._id",
                    "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "date": "$time_period"}},
                    "month": {"$dateToString": {"format": "%Y-%m", "date": "$time_period"}},
                    "air_temperature": "$air_temperature",
                },
            },
            {
                "$sort": {"station": 1, "timestamp": 1},
            },
            {
                "$group": {
                    "_id": ["$station", "$month"],
                    "measurements": {
                        "$push": {
                            "timestamp": "$timestamp",
                            "air_temperature": "$air_temperature",
                        },
                    },
                    "count": {"$sum": 1}

                },
            },
            {
                "$sort": {"_id.0": 1, "_id.1": 1},
            },
        ]

        logger.info('Pipeline for temperature data started.')
        data = MeasurementDocument.objects().aggregate(temperature_pipeline)
        for batch in data:
            (station, *_), batch_size, measurements = batch.get('_id'), batch.get('count'), batch.get('measurements')

            with Temperature.bulk_objects.bulk_update_or_create_context(
                    match_field=('station_id', 'timestamp'),
                    update_fields=('temperature',),
                    batch_size=batch_size,
            ) as bulk:
                for measurement in measurements:
                    bulk.queue(Temperature(
                        station_id=station,
                        timestamp=dateparse.parse_datetime(measurement['timestamp']),
                        temperature=measurement['air_temperature'],
                    ))

            logger.info('Computed and imported %s records.', batch_size)

        rainfall_pipeline = [
            {
                "$match": {
                    "rainfall_24hr": {"$ne": None},
                },
            },
            {
                "$lookup":
                    {
                        "from": 'station',
                        "localField": 'station',
                        "foreignField": '_id',
                        "as": 'station',
                    },
            },
            {
                "$unwind": {"path": '$station'},
            },
            {
                "$project": {
                    "station": "$station._id",
                    "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "date": "$rainfall_24hr.end_time"}},
                    "rainfall": "$rainfall_24hr.value",
                },
            },
            {
                "$sort": {"station": 1, "timestamp": 1},
            },
            {
                "$group": {
                    "_id": ["$station", "$timestamp"],
                    "rainfall": {"$first": "$rainfall"}

                },
            },
            {
                "$sort": {"_id.0": 1, "_id.1": 1},
            },
        ]

        logger.info('Pipeline for rainfall data started.')
        data = MeasurementDocument.objects().aggregate(rainfall_pipeline)
        for batch in data:
            (station, timestamp), rainfall_measurement = batch.get('_id'), batch.get('rainfall')

            Rainfall.objects.update_or_create(
                station_id=station,
                timestamp=dateparse.parse_datetime(timestamp),
                rainfall=rainfall_measurement,
            )


__all__ = ['Computer']
