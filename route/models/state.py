from django.db import models
from utils.models import TimeStampedModel
import uuid
from simple_history.models import HistoricalRecords


class State(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    hindi_name = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"


class StateName(TimeStampedModel):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    english = models.CharField(max_length=255, null=True, blank=True)
    hindi = models.CharField(max_length=255, null=True, blank=True)
    gujarati = models.CharField(max_length=255, null=True, blank=True)
    telugu = models.CharField(max_length=255, null=True, blank=True)
    tamil = models.CharField(max_length=255, null=True, blank=True)
    kannada = models.CharField(max_length=255, null=True, blank=True)
    punjabi = models.CharField(max_length=255, null=True, blank=True)
    history = HistoricalRecords()
