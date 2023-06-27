import uuid
from django.db import models
from bus.models.bus import Bus
from route.models.route import Route
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class BusRouteReturn(TimeStampedModel):

    RETURN_TYPE = (
        'Today',
        'Alternate'
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    from_town = models.CharField(max_length=255, default='from town')
    to_town = models.CharField(max_length=255, default='to town')
    start_time = models.TimeField(default='00:00:00')
    arrival_time = models.TimeField(default='00:00:00')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    route_return_type = models.CharField(
        max_length=20, choices=RETURN_TYPE, default='Select')
    history = HistoricalRecords()

    def __str__(self):
        return self.id
