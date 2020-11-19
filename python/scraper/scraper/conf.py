from models import RainfallDocument, LimitTemperatureDocument, MaximumGustSpeedDocument, MaximumGustDirectionDocument

pass_e = lambda e: e
el_v = lambda data_type: lambda e: data_type(e.get("#text"))
rainfall = lambda e: RainfallDocument(
    start_time=str(e.get("@start-time-utc")),
    end_time=str(e.get("@end-time-utc")),
    units=str(e.get("@units")),
    value=el_v(float)(e)
)
temperature = lambda e: LimitTemperatureDocument(
    start_time=str(e.get("@start-time-utc")),
    end_time=str(e.get("@end-time-utc")),
    timestamp=str(e.get("@time-utc")),
    units=str(e.get("@units")),
    value=el_v(float)(e)
)
speed = lambda e: MaximumGustSpeedDocument(
    start_time=str(e.get("@start-time-utc")),
    end_time=str(e.get("@end-time-utc")),
    timestamp=str(e.get("@time-utc")),
    units=str(e.get("@units")),
    value=el_v(float)(e)
)
direction = lambda e: MaximumGustDirectionDocument(
    start_time=str(e.get("@start-time-utc")),
    end_time=str(e.get("@end-time-utc")),
    timestamp=str(e.get("@time-utc")),
    value=el_v(str)(e)
)


MEASUREMENT_ATTRS_MAPPING = {
    'time_period': el_v(str),
    'apparent_temp': el_v(float),
    'cloud': el_v(str),
    'cloud_oktas': el_v(int),
    'cloud_type_id': el_v(int),
    'delta_t': el_v(float),
    'air_temperature': el_v(float),
    'dew_point': el_v(float),
    'pres': el_v(float),
    'msl_pres': el_v(float),
    'qnh_pres': el_v(float),
    'rain_hour': el_v(float),
    'rain_ten': el_v(float),
    'rel_humidity': el_v(int),
    'vis_km': el_v(float),
    'weather': el_v(str),
    'wind_dir': el_v(str),
    'wind_dir_deg': el_v(int),
    'wind_spd_kmh': el_v(int),
    'wind_spd': el_v(int),
    'gust_kmh': el_v(int),
    'wind_gust_spd': el_v(int),

    'rainfall': rainfall,
    'rainfall_24hr': rainfall,
    'maximum_air_temperature': temperature,
    'minimum_air_temperature': temperature,
    'maximum_gust_spd': speed,
    'maximum_gust_kmh': speed,
    'maximum_gust_dir': direction,
}

MEASUREMENT_ATTRS_TO_SKIP = set(
    'cloud_base_m cloud_type sea_height trend_pres swell_dir swell_height swell_period trend_pres'
    .split(' ')
)

__all__ = ['MEASUREMENT_ATTRS_MAPPING', 'MEASUREMENT_ATTRS_TO_SKIP']