import django

django.setup()

from . import models
from .documents import MeasurementDocument, StationDocument, RainfallDocument, LimitTemperatureDocument, MaximumGustSpeedDocument, MaximumGustDirectionDocument

__all__ = [
    'MeasurementDocument',
    'StationDocument',
    'RainfallDocument',
    'LimitTemperatureDocument',
    'MaximumGustSpeedDocument',
    'MaximumGustDirectionDocument',
    'models',
]
