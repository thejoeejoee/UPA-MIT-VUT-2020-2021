import django

django.setup()

from . import models
from .documents import MeasurementDocument, StationDocument

__all__ = [
    'MeasurementDocument',
    'StationDocument',
    'models',
]
