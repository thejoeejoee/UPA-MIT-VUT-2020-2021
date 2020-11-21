from django.utils import dateparse

from models import MeasurementDocument
from models.models import Temperature, Rainfall
from .syncer import Syncer


class Computer(object):

    def run(self):
        Syncer.sync_stations()

        average_day_temperature_pipeline = [
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
                    "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time_period"}},
                    "station_id": "$station._id",
                    "air_temperature": "$air_temperature",
                },
            },
            {
                "$group": {
                    "_id": {
                        "day": "$day",
                        "station_id": "$station_id",
                    },

                    "avg_air_temperature": {"$avg": "$air_temperature"},
                },
            },
            {
                "$sort": {"_id.day": 1, "_id.station_id": 1},
            },
        ]

        tempereture_pipeline = [
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
                    # "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "timezone": "$station.location", "date": "$time_period"}},
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

        data = MeasurementDocument.objects().aggregate(tempereture_pipeline)
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

        rainfall_pipeline = [
            {
                "$match": {
                    "rainfall_24hr": {"$ne": None},
                    "rainfall": {"$ne": None},
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
                    # "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "timezone": "$station.location", "date": "$rainfall.end_time"}},
                    "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "date": "$rainfall.end_time"}},
                    "month": {"$dateToString": {"format": "%Y-%m", "date": "$time_period"}},
                    "rainfall_from_9": "$rainfall.value",
                    "rainfall_24hr_to_9": "$rainfall_24hr.value",
                },
            },
            {
                "$sort": {"_id": 1, "timestamp": 1},
            },
            {
                "$group": {
                    "_id": ["$station", "$month"],
                    "measurements": {
                        "$push": {
                            "timestamp": "$timestamp",
                            "rainfall_from_9": "$rainfall_from_9",
                            "rainfall_24hr_to_9": "$rainfall_24hr_to_9",
                        },
                    },
                    "count": {"$sum": 1}

                },
            },
            {
                "$sort": {"_id.0": 1, "_id.1": 1},
            },
        ]

        data = MeasurementDocument.objects().aggregate(rainfall_pipeline)
        for batch in data:
            (station, *_), batch_size, measurements = batch.get('_id'), batch.get('count'), batch.get('measurements')

            with Rainfall.bulk_objects.bulk_update_or_create_context(
                    update_fields=('rainfall_from_morning', 'rainfall_last_day'),
                    match_field=('station_id', 'timestamp'),
                    batch_size=batch_size
            ) as bulk:
                for measurement in measurements:
                    bulk.queue(Rainfall(
                        station_id=station,
                        timestamp=dateparse.parse_datetime(measurement['timestamp']),
                        rainfall_from_morning=measurement['rainfall_from_9'],
                        rainfall_last_day=measurement['rainfall_24hr_to_9'],
                    ))


__all__ = ['Computer']
