from models import MeasurementDocument
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

        tempereture_ranking_pipeline = [
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
                    "station_id": "$station._id",
                    "air_temperature": "$air_temperature",
                },
            },
            {
                "$group": {
                    "_id": {
                        "station_id": "$station_id",
                    },

                    "avg_air_temperature": {"$avg": "$air_temperature"},
                },
            },
            {
                "$sort": {"avg_air_temperature": 1},
            },
        ]

        rainfall_ranking_pipeline = [
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
                    "station_id": "$station._id",
                    "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$time_period"}},
                    "time": {"$dateToString": {"format": "%H:%M:%S", "date": "$time_period"}},
                    "history_rainfall": { "$ifNull": [ { "$toDouble": "$rainfall_24hr.#text" }, 0.0]} ,
                    "actual_rainfall": { "$ifNull": [ { "$toDouble": "$rainfall.#text" }, 0.0]},
                },
            },
            {
                "$sort": {"station_id": 1, "day": 1, "time": 1},
            },
            {
                "$group": {
                    "_id": {
                        "station_id": "$station_id",
                        "day": "$day",
                    },

                    "time": {"$last": "$time"},
                    "history_rainfall": {"$last": "$history_rainfall"},
                    "actual_rainfall": {"$last": "$actual_rainfall"},
                },
            },
            {
                "$group": {
                    "_id": {
                        "station_id": "$_id.station_id",
                    },
                    "all_history_rainfalls": {"$sum": "$history_rainfall"},
                    "last_rainfall": {"$last": "$actual_rainfall"},
                },
            },
            {
                "$project": {
                    "_id": "$_id",
                    "rainfalls": { "$add": [ "$all_history_rainfalls", "$last_rainfall" ] },
                },
            },
            {
                "$sort": {"rainfalls": 1},
            },
        ]

        data = MeasurementDocument.objects().aggregate(average_day_temperature_pipeline)
        for item in data:
            print(item)


__all__ = ['Computer']
