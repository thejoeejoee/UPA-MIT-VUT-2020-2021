from mongoengine import Document, EmbeddedDocument, ReferenceField, DictField, StringField, FloatField, DateTimeField, IntField, EmbeddedDocumentField

class StationDocument(Document):
    meta = dict(
        collection='station',
        ordering=['wmo_id'],
    )

    wmo_id = IntField(primary_key=True)
    location = StringField()
    station_name = StringField()
    station_height = FloatField()
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self):
        return f'{self.wmo_id}: {self.station_name} ({self.latitude}, {self.longitude}; {self.station_height})'

class PeriodDocument():
    start_time = DateTimeField()
    end_time = DateTimeField()

class RainfallDocument(PeriodDocument, EmbeddedDocument):
    units = StringField()
    value = FloatField()

class LimitTemperatureDocument(PeriodDocument, EmbeddedDocument):
    timestamp = DateTimeField()
    units = StringField()
    value = FloatField()

class MaximumGustSpeedDocument(PeriodDocument, EmbeddedDocument):
    timestamp = DateTimeField()
    units = StringField()
    value = FloatField()

class MaximumGustDirectionDocument(PeriodDocument, EmbeddedDocument):
    timestamp = DateTimeField()
    value = StringField()

class MeasurementDocument(Document):
    meta = dict(
        collection='measurement',
        ordering=['time_period'],
    )

    station = ReferenceField(StationDocument, required=True)
    time_period = DateTimeField()
    apparent_temp = FloatField()
    cloud = StringField()
    cloud_oktas = IntField()
    cloud_type_id = IntField()
    delta_t = FloatField()
    air_temperature = FloatField()
    dew_point = FloatField()
    pres = FloatField()
    msl_pres = FloatField()
    qnh_pres = FloatField()
    rain_hour = FloatField()
    rain_ten = FloatField()
    rel_humidity = IntField()
    vis_km = FloatField()
    weather = StringField()
    wind_dir = StringField()
    wind_dir_deg = IntField()
    wind_spd_kmh = IntField()
    wind_spd = IntField()
    gust_kmh = IntField()
    wind_gust_spd = IntField()
    rainfall = EmbeddedDocumentField(RainfallDocument)
    rainfall_24hr = EmbeddedDocumentField(RainfallDocument)
    maximum_air_temperature = EmbeddedDocumentField(LimitTemperatureDocument)
    minimum_air_temperature = EmbeddedDocumentField(LimitTemperatureDocument)
    maximum_gust_spd = EmbeddedDocumentField(MaximumGustSpeedDocument)
    maximum_gust_kmh = EmbeddedDocumentField(MaximumGustSpeedDocument)
    maximum_gust_dir = EmbeddedDocumentField(MaximumGustDirectionDocument)
