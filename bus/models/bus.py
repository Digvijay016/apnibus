import uuid
from django.db import models
from utils.models import TimeStampedModel
# from account.models.operator import Operator
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator


class Bus(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_number = models.CharField(max_length=255, unique=True)
    pos_serial_no = models.CharField(max_length=255,null=True, blank=True)
    pos_dsn_number = models.CharField(max_length=255, null=True, blank=True)
    gps_sim_image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.number


class BusPhotograph(TimeStampedModel):
    BUS_PHOTOGRAPH = 'bus_photograph'
    RC = 'rc'

    PHOTOGRAPH_TYPE = (
        (BUS_PHOTOGRAPH, 'bus_photograph'),
        (RC, 'rc')
    )

    bus_photograph_id = models.UUIDField(default=uuid.uuid1, editable=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    photograph = models.FileField(upload_to='bus/', null=True, blank=True)
    description = models.TextField(null=True)
    type = models.CharField(max_length=255, choices=PHOTOGRAPH_TYPE)
    history = HistoricalRecords()

    def __str__(self):
        return self.id
