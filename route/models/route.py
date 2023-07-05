from django.db import models
from utils.models import TimeStampedModel
from .town import Town
import uuid
from simple_history.models import HistoricalRecords


class Route(TimeStampedModel):
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
    from_town = models.ForeignKey(
        Town, on_delete=models.PROTECT, related_name="route_from_town", blank=True)
    to_town = models.ForeignKey(
        Town, on_delete=models.PROTECT, related_name="route_to_town", blank=True)
    name = models.CharField(max_length=255, blank=True)
    via = models.CharField(max_length=255, default="")
    is_default = models.BooleanField(default=False)
    status = models.CharField(max_length=255, choices=STATUS, default=ACTIVE)
    reverse_route_exists = models.BooleanField(default=False)
    history = HistoricalRecords()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['from_town', 'to_town', 'via'], name="from_town_via_to_town"),
    #     ]

    def __str__(self):
        return self.from_town.name + "-" + self.to_town.name
