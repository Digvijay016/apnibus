import uuid
from django.db import models
from utils.models import TimeStampedModel
from bus.models.bus_route import BusRoute
from simple_history.models import HistoricalRecords


class BusRouteJourney(TimeStampedModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    REQUEST_FOR_DELETION = 'request_for_deletion'
    DELETION_READY = 'deletion_ready'
    SCHEDULED = "scheduled"
    STARTED = "started"
    COMPLETED = "completed"

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
        (REQUEST_FOR_DELETION, 'request_for_deletion'),
        (DELETION_READY, 'deletion_ready'),
        (SCHEDULED, "scheduled"),
        (STARTED, "started"),
        (COMPLETED, "completed")
    )

    DEFAULT = 'default'
    GMAPS = 'gmaps'
    GPS = 'gps'
    CALCULATED_START_TIME_TYPE = (
        (DEFAULT, 'default'),
        (GMAPS, 'gmaps'),
        (GPS, 'gps')
    )

    COMPLETED = 'completed'
    FAILED = 'failed'
    IN_PROGRESS = 'in_progress'

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # start_time = models.DateTimeField()
    # calculated_start_time = models.TimeField(null=True)
    # is_active = models.BooleanField(default=True)
    # status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    # gps_status = models.BooleanField(default=False)
    # calculated_start_time_type = models.CharField(max_length=50, null=True, choices=CALCULATED_START_TIME_TYPE)
    # gps_status_active_till = models.DateTimeField(null=True)
    # is_settled = models.BooleanField(default=False)
    # journey_extender_status = models.CharField(max_length=50, null=True)
    #
    # # Adding this boolean to identify journeys created after our fix of missing busroutejourney
    # created_late = models.BooleanField(default=False)
    history = HistoricalRecords()
