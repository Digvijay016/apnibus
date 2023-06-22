from django.db import models
from utils.models import TimeStampedModel
from .state import State
import uuid
from simple_history.models import HistoricalRecords


class District(TimeStampedModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    hindi_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.state} - {self.name}"

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "District"

        constraints = [
            models.UniqueConstraint(fields=['state', 'name'], name="state_district_name"),
        ]


class DistrictName(TimeStampedModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    english = models.CharField(max_length=255, null=True, blank=True)
    hindi = models.CharField(max_length=255, null=True, blank=True)
    gujarati = models.CharField(max_length=255, null=True, blank=True)
    telugu = models.CharField(max_length=255, null=True, blank=True)
    tamil = models.CharField(max_length=255, null=True, blank=True)
    kannada = models.CharField(max_length=255, null=True, blank=True)
    punjabi = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()
