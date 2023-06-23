import uuid
from django.db import models
from utils.models import TimeStampedModel
from bus.models.bus_route_town import BusRouteTown
from route.models.route_town_stoppage import RouteTownStoppage
from simple_history.models import HistoricalRecords


class BusRouteTownStoppage(TimeStampedModel):
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
    bus_route_town = models.ForeignKey(
        BusRouteTown, on_delete=models.CASCADE, null=True, related_name='bus_route_town')
    route_town_stoppage = models.ForeignKey(
        RouteTownStoppage, on_delete=models.CASCADE, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    duration = models.IntegerField(null=True)
    start_time = models.TimeField(null=True)
    # calculated_duration = models.IntegerField(null=True)
    calculated_start_time = models.TimeField(null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    eta_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return self.id
