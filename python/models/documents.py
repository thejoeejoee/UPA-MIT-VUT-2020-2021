from mongoengine import Document, ReferenceField, DictField, StringField, FloatField, DateTimeField, IntField


class StationDocument(Document):
    meta = dict(collection='station')

    wmo_id = IntField(primary_key=True)
    location = StringField()
    station_name = StringField()
    station_height = FloatField()
    latitude = FloatField()
    longitude = FloatField()

    def __str__(self):
        return f'{self.wmo_id}: {self.station_name} ({self.latitude}, {self.longitude}; {self.station_height})'


class MeasurementDocument(Document):
    meta = dict(collection='measurement')

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
    rainfall = DictField()
    rainfall_24hr = DictField()
    maximum_air_temperature = DictField()
    minimum_air_temperature = DictField()
    maximum_gust_spd = DictField()
    maximum_gust_kmh = DictField()
    maximum_gust_dir = DictField()
