from django.db import models
from utils.models import TimeStampedModel
from .district import District
from .city import City
import uuid
from simple_history.models import HistoricalRecords


class Town(TimeStampedModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive')
    )

    CITY = 'CITY'
    TOWN = 'TOWN'
    VILLAGE = 'VILLAGE'

    TYPE = (
        (CITY, CITY),
        (TOWN, TOWN),
        (VILLAGE, VILLAGE)
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    pincode = models.CharField(max_length=255, blank=True)
    short_name = models.CharField(max_length=255, blank=True)
    hindi_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    type = models.CharField(max_length=20, choices=TYPE, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.district} - {self.name}"

    class Meta:
        verbose_name = "Town"
        verbose_name_plural = "Towns"

        constraints = [
            models.UniqueConstraint(
                fields=['district', 'name'], name="district_town_name"),
        ]


class TownName(TimeStampedModel):
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    english = models.CharField(max_length=255, blank=True)
    hindi = models.CharField(max_length=255, blank=True)
    gujarati = models.CharField(max_length=255, blank=True)
    telugu = models.CharField(max_length=255, blank=True)
    tamil = models.CharField(max_length=255, blank=True)
    kannada = models.CharField(max_length=255, blank=True)
    punjabi = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()
