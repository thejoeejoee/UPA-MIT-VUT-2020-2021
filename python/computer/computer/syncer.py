from logging import getLogger

from models import StationDocument
from models.models import Station

logger = getLogger(__name__)


class Syncer:
    @staticmethod
    def sync_stations():
        attrs_to_sync = ('location', 'station_name', 'station_height', 'latitude', 'longitude')

        logger.info('Syncing stations from mongo to postgres started.')

        synced = []
        for station_doc in StationDocument.objects():  # type: StationDocument
            station_model, created = Station.objects.update_or_create(
                defaults={
                    k: getattr(station_doc, k)
                    for k in attrs_to_sync
                },
                wmo_id=station_doc.wmo_id,
            )
            synced.append(created)
            logger.debug('Station %s synced to %s, created: %s.', station_doc, station_model, created)

        logger.info('Synced total %s stations, %s created.', len(synced), len(tuple(filter(None, synced))))
