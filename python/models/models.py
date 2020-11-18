from django.db import models


class Station(models.Model):
    wmo_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=128)
    station_name = models.CharField(max_length=128)
    station_height = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.wmo_id}: {self.station_name} ({self.latitude}, {self.longitude}; {self.station_height})'

# TODO: models for each computer result