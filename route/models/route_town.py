from django.db import models
from utils.models import TimeStampedModel
from route.models.town import Town
from route.models.route import Route
import uuid
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


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
        "route.Route", on_delete=models.CASCADE, blank=True)
    town = models.ForeignKey(
        "route.Town", on_delete=models.PROTECT, blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['route', 'town'], name="UC_route_town")
        ]

    def __str__(self):
        return f"{self.route} + -> + {self.town.name}"
