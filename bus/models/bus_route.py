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
    # bus_number = models.CharField(
    #     max_length=255, unique=True, default='APNI_BUS')
    from_town = models.CharField(max_length=255, default='from town')
    to_town = models.CharField(max_length=255, default='to town')
    start_time = models.TimeField(default='00:00:00')
    arrival_time = models.TimeField(default='00:00:00')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.bus.number) + " --> " + str(self.from_town) + str(self.to_town) + str(self.departure_time) + str(self.arrival_time)

    def __str__(self):
        return self.id
