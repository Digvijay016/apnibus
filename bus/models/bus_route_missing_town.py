import uuid
from django.db import models
from utils.models import TimeStampedModel
from bus.models.bus_route import BusRoute
from simple_history.models import HistoricalRecords


class BusRouteMissingTown(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, db_column='created_on')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    bus_route = models.ForeignKey("bus.BusRoute", on_delete=models.CASCADE, null=True, blank=True)
    missing_town = models.CharField(
        max_length=255, default='town', blank=True)
    duration = models.IntegerField(default = 0,blank=True)
    history = HistoricalRecords()