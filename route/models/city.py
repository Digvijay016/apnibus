import uuid
from django.db import models
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class City(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    hindi_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"City - {self.name}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
