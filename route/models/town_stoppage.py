from django.db import models
from utils.models import TimeStampedModel
from route.models.town import Town
import uuid
from simple_history.models import HistoricalRecords


class TownStoppage(TimeStampedModel):
    # Stoppage type
    MAJOR = 'major'
    MINOR = 'minor'

    STOPPAGE_TYPES = (
        (MAJOR, 'major'),
        (MINOR, 'minor')
    )

    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    radius = models.FloatField(blank=True)
    type = models.CharField(
        max_length=5, choices=STOPPAGE_TYPES, default=MAJOR)
    hindi_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return self.town.name + '--' + self.name

    class Meta:
        verbose_name = "TownStoppage"
        verbose_name_plural = "TownStoppages"

        constraints = [
            models.UniqueConstraint(
                fields=['town', 'name'], name="town_stoppage_name"),
        ]


class TownStoppageName(TimeStampedModel):
    town_stoppage = models.ForeignKey(
        TownStoppage, on_delete=models.CASCADE, related_name='town_stoppage_name')
    english = models.CharField(max_length=255, blank=True)
    hindi = models.CharField(max_length=255, blank=True)
    gujarati = models.CharField(max_length=255, blank=True)
    telugu = models.CharField(max_length=255, blank=True)
    tamil = models.CharField(max_length=255, blank=True)
    kannada = models.CharField(max_length=255, blank=True)
    punjabi = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()
