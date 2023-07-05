import uuid
from django.db import models
from route.models.route_town import RouteTown
from utils.models import TimeStampedModel
# from route.models.route_town import RouteTown
from route.models.town_stoppage import TownStoppage
from simple_history.models import HistoricalRecords


class RouteTownStoppage(TimeStampedModel):
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
    route_town = models.ForeignKey(
        RouteTown, on_delete=models.CASCADE, blank=True)
    town_stoppage = models.ForeignKey(
        TownStoppage, on_delete=models.PROTECT, blank=True)
    duration = models.IntegerField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['route_town', 'town_stoppage'], name="UC_route_town_town_stpg"),
            models.UniqueConstraint(
                fields=['route_town', 'duration'], name="UC_route_town_duration"),

        ]
