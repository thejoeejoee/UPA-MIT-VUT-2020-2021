from models import MeasurementDocument
from models.models import Station, Temperature, Rainfall
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
                    "_id": "$station._id",
                    # "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "timezone": "$station.location", "date": "$time_period"}},
                    "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "date": "$time_period"}},
                    "air_temperature": "$air_temperature",
                },
            },
            {
                "$sort": {"_id": 1, "timestamp": 1},
            },
        ]

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
                    "_id": "$station._id",
                    # "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "timezone": "$station.location", "date": "$rainfall.end_time"}},
                    "timestamp": {"$dateToString": {"format": "%Y-%m-%dT%H:%M:%S%z", "date": "$rainfall.end_time"}},
                    "rainfall_from_9": "$rainfall.value",
                    "rainfall_24hr_to_9": "$rainfall_24hr.value",
                },
            },
            {
                "$sort": {"_id": 1, "timestamp": 1},
            },
        ]

        data = MeasurementDocument.objects().aggregate(tempereture_pipeline)
        for item in data:
            station = Station.objects.get(wmo_id=item['_id'])
            Temperature.objects.update_or_create(station=station, timestamp=item['timestamp'], temperature=item['air_temperature'])
        
        data = MeasurementDocument.objects().aggregate(rainfall_pipeline)
        for item in data:
            station = Station.objects.get(wmo_id=item['_id'])
            Rainfall.objects.update_or_create(station=station, timestamp=item['timestamp'], rainfall_from_morning=item['rainfall_from_9'], rainfall_last_day=item['rainfall_24hr_to_9'])


__all__ = ['Computer']
