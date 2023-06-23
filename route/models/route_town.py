from django.db import models
from utils.models import TimeStampedModel
from route.models.town import Town
from route.models.route import Route
import uuid
from simple_history.models import HistoricalRecords


class RouteTown(TimeStampedModel):
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
        Route, on_delete=models.CASCADE, null=True, blank=True)
    town = models.ForeignKey(
        Town, on_delete=models.PROTECT, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['route', 'town'], name="UC_route_town")
        ]

    def __str__(self):
        return str(self.route) + "->" + self.town.name
