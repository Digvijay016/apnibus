import uuid
from django.db import models
from utils.models import TimeStampedModel
# from bus.models import BusRouteJourney, BusRouteTownStoppage
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from simple_history.models import HistoricalRecords


class BusRouteTownStoppageJourney(TimeStampedModel):

    APPROACHING = 'approaching'
    INSIDE = 'inside'
    DEPARTED = 'departed'
    GPS_OUTAGE = 'gps_outage'
    SKIPPED = 'skipped'
    IN_QUEUE = 'in_queue'

    GEOFENCE_STATUS_TYPE = (
        (APPROACHING, 'approaching'),
        (INSIDE, 'inside'),
        (DEPARTED, 'departed'),
        (GPS_OUTAGE, 'gps_outage'),
        (SKIPPED, 'skipped'),
        (IN_QUEUE, 'in_queue')
    )

    DEFAULT = 'default'
    GMAPS = 'gmaps'
    GPS = 'gps'

    ARRIVAL_TIME_TYPE = (
        (DEFAULT, 'default'),
        (GMAPS, 'gmaps'),
        (GPS, 'gps')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # bus_route_journey = models.ForeignKey(BusRouteJourney, on_delete=models.CASCADE)
    bus_route_town_stoppage = models.ForeignKey(
        BusRouteTownStoppage, on_delete=models.CASCADE, related_name='bus_route_town_stoppage')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    geofence_status = models.CharField(
        max_length=25, null=True, choices=GEOFENCE_STATUS_TYPE)
    arrival_time_type = models.CharField(
        max_length=50, null=True, choices=ARRIVAL_TIME_TYPE)

    gps_time = models.DateTimeField(null=True)
    gmaps_time = models.DateTimeField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.id


"""

Cron Jobs:
Journey - Bus Adda  --> Inside (arrival time) --> update all future BusAdda Journey --> 
where duration is 0  (first stoppage of a town) --> update the same in BusViaRouteJourney for future journeys

Journey Extender:

"""
