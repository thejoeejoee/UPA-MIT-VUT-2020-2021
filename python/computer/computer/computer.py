from models import MeasurementDocument
from .syncer import Syncer


class Computer(object):

    def run(self):
        Syncer.sync_stations()

        pipeline = [
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
        data = MeasurementDocument.objects().aggregate(pipeline)

        for item in data:
            print(item)


__all__ = ['Computer']
