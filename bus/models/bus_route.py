from django.utils import timezone
import uuid
from django.db import models
from utils.models import TimeStampedModel
from .bus import Bus
from route.models.route import Route
from simple_history.models import HistoricalRecords


class BusRoute(TimeStampedModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    REQUEST_FOR_DELETION = 'request_for_deletion'
    DELETION_READY = 'deletion_ready'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
        (REQUEST_FOR_DELETION, 'request_for_deletion'),
        (DELETION_READY, 'deletion_ready')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_number = models.CharField(
        max_length=255, unique=True, default='APNI_BUS')
    from_town = models.CharField(max_length=255, default='from town')
    to_town = models.CharField(max_length=255, default='to town')
    departure_time = models.TimeField(default='00:00:00')
    arrival_time = models.TimeField(default='00:00:00')
    # bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    # route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    # start_time = models.TimeField(null=True)

    # calculated time would be null incase we don't have synced with the gps past data
    # calculated_start_time = models.TimeField(null=True)
    # interval = models.IntegerField(null=True)
    # is_active = models.BooleanField(default=False)
    # status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    # is_base_route = models.BooleanField(default=True)
    # name = models.CharField(max_length=255, null=True, blank=True)
    # updating_time = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.bus.number) + " --> " + str(self.from_town) + str(self.to_town) + str(self.departure_time) + str(self.arrival_time)
