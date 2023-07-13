import uuid
from django.db import models
from utils.models import TimeStampedModel
from bus.models.bus_route_town import BusRouteTown
from route.models.route_town_stoppage import RouteTownStoppage
from simple_history.models import HistoricalRecords


class BusRouteTownStoppage(models.Model):
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
    created_on = models.DateTimeField(auto_now_add=True, db_column='created_on')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    bus_route_town = models.ForeignKey(
        "bus.BusRouteTown", on_delete=models.CASCADE, blank=True, related_name='bus_route_town')
    route_town_stoppage = models.ForeignKey(
        "route.RouteTownStoppage", on_delete=models.CASCADE, blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    duration = models.IntegerField(blank=True)
    start_time = models.TimeField(blank=True)
    calculated_duration = models.IntegerField(blank=True)
    calculated_start_time = models.TimeField(blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    eta_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)
