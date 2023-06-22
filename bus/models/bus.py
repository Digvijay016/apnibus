import uuid
from django.db import models
from utils.models import TimeStampedModel
# from account.models.operator import Operator
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator


class Bus(TimeStampedModel):
    # SEATER = 'seater'
    # SLEEPER = 'sleeper'
    # SEATER_SLEEPER = 'seater_sleeper'
    # UPPER_SINGLE_SLEEPER = 'upper_single_sleeper'
    # UPPER_SHARING_SLEEPER = 'upper_sharing_sleeper'
    # RECLINER = 'recliner'
    #
    # SEAT_TYPE = (
    #     (SEATER, 'seater'),
    #     (SLEEPER, 'sleeper'),
    #     (SEATER_SLEEPER, 'seater_sleeper'),
    #     (UPPER_SINGLE_SLEEPER, 'upper_single_sleeper'),
    #     (UPPER_SHARING_SLEEPER, 'upper_sharing_sleeper'),
    #     (RECLINER, 'recliner')
    # )
    #
    # LAYOUT_1 = '2+1'
    # LAYOUT_2 = '2+2'
    # LAYOUT_3 = '1+2'
    # LAYOUT_4 = '2+3'
    # LAYOUT_5 = '3+3'
    #
    # LAYOUT_TYPES = (
    #     (LAYOUT_1, '2+1'),
    #     (LAYOUT_2, '2+2'),
    #     (LAYOUT_3, '1+2'),
    #     (LAYOUT_4, '2+3'),
    #     (LAYOUT_5, '3+3')
    # )
    #
    # GENERAL = "general"
    # EXPRESS = "express"
    # LUXURY = "luxury"
    #
    # BUS_CATEGORY = (
    #     (GENERAL, "general"),
    #     (EXPRESS, "express"),
    #     (LUXURY, "luxury"),
    # )
    #
    # ONBOARDED = 'onboarded'
    # ACTIVE = 'active'
    # INACTIVE = 'inactive'
    #
    # BUS_STATUS = (
    #     (ONBOARDED, 'onboarded'),
    #     (ACTIVE, 'active'),
    #     (INACTIVE, 'inactive'),
    # )
    #
    # IN_PROGRESS = 'in_progress'
    # INSTALLED = 'installed'
    # NOT_INSTALLED = 'not_installed'
    # FAULTY = 'faulty'
    # LIVE = 'live'
    #
    # GPS_STATUS = (
    #     (IN_PROGRESS, 'in_progress'),
    #     (INSTALLED, 'installed'),
    #     (NOT_INSTALLED, 'not_installed'),
    #     (FAULTY, 'faulty'),
    #     (LIVE, 'live')
    # )
    #
    # COMMISSION_VALIDATOR = [
    #     MaxValueValidator(30),
    #     MinValueValidator(0)
    # ]
    #
    # PERCENTAGE = 'percentage'
    # FIXED = 'fixed'
    # BOOKING_OFF = 'booking_off'
    #
    # ONLINE_APP_BOOKING_COMMISSION = (
    #     (PERCENTAGE, 'percentage'),
    #     (FIXED, 'fixed'),
    #     (BOOKING_OFF, 'booking_off'),
    # )
    #
    # FULL_AMOUNT = 'full_amount'
    #
    # QR_BOOKING_COMMISSION = (
    #     (FULL_AMOUNT, 'full_amount'),
    #     (BOOKING_OFF, 'booking_off')
    # )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_number = models.CharField(max_length=255, unique=True)
    pos_serial_no = models.FileField(upload_to='bus/', null=True, blank=True)
    pos_dsn_number = models.CharField(max_length=255, null=True, blank=True)
    gps_sim_image = models.FileField(upload_to='bus/', null=True, blank=True)

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

