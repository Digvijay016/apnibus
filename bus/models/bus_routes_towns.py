import uuid
from django.db import models
from bus.models.bus_route_missing_town import BusRouteMissingTown
from route.models.route import Route
from route.models.town import Town
from route.models.route_town_stoppage import RouteTownStoppage
from route.models.town_stoppage import TownStoppage
from utils.models import TimeStampedModel
from route.models.route_town import RouteTown
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class BusRoutesTowns(TimeStampedModel):
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
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, blank=True)
    duration = models.IntegerField(blank=True)
    calculated_duration = models.IntegerField(blank=True)
    towns = models.JSONField(default=list, blank=True)
    day = models.IntegerField(blank=True, default=0)
    town_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    town_stoppage_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    eta_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)