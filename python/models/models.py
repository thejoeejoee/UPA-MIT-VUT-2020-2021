from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class BaseModel(models.Model):
    created = CreationDateTimeField()

    objects = models.Manager()
    bulk_objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        abstract = True


class Station(BaseModel):
    wmo_id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=128)
    station_name = models.CharField(max_length=128)
    station_height = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'station'
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'

    def __str__(self):
        return f'{self.wmo_id}: {self.station_name} ({self.latitude}, {self.longitude}; {self.station_height})'


class BaseTimedStationDataModel(BaseModel):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    class Meta:
        abstract = True
        unique_together = (
            ('station', 'timestamp'),
        )
        ordering = ('timestamp', 'station')


class Temperature(BaseTimedStationDataModel):
    temperature = models.FloatField()

    class Meta(BaseTimedStationDataModel.Meta):
        db_table = 'temperature'
        verbose_name = 'Temperature'
        verbose_name_plural = 'Temperatures'

    def __str__(self):
        return f'{self.station}: ({self.timestamp}, {self.temperature})'


class Rainfall(BaseTimedStationDataModel):
    rainfall = models.FloatField()

    class Meta(BaseTimedStationDataModel.Meta):
        db_table = 'rainfall'
        verbose_name = 'Rainfall'
        verbose_name_plural = 'Rainfalls'

    def __str__(self):
        return f'{self.station}: ({self.timestamp}, {self.rainfall})'
