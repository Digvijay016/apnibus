import uuid
from django.db import models
from utils.models import TimeStampedModel
from account.models.operators import Operator
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, MinValueValidator


class Bus(TimeStampedModel):
    SEATER = 'seater'
    SLEEPER = 'sleeper'
    SEATER_SLEEPER = 'seater_sleeper'
    UPPER_SINGLE_SLEEPER = 'upper_single_sleeper'
    UPPER_SHARING_SLEEPER = 'upper_sharing_sleeper'
    RECLINER = 'recliner'

    SEAT_TYPE = (
        (SEATER, 'seater'),
        (SLEEPER, 'sleeper'),
        (SEATER_SLEEPER, 'seater_sleeper'),
        (UPPER_SINGLE_SLEEPER, 'upper_single_sleeper'),
        (UPPER_SHARING_SLEEPER, 'upper_sharing_sleeper'),
        (RECLINER, 'recliner')
    )

    LAYOUT_1 = '2+1'
    LAYOUT_2 = '2+2'
    LAYOUT_3 = '1+2'
    LAYOUT_4 = '2+3'
    LAYOUT_5 = '3+3'

    LAYOUT_TYPES = (
        (LAYOUT_1, '2+1'),
        (LAYOUT_2, '2+2'),
        (LAYOUT_3, '1+2'),
        (LAYOUT_4, '2+3'),
        (LAYOUT_5, '3+3')
    )

    GENERAL = "general"
    EXPRESS = "express"
    LUXURY = "luxury"

    BUS_CATEGORY = (
        (GENERAL, "general"),
        (EXPRESS, "express"),
        (LUXURY, "luxury"),
    )

    ONBOARDED = 'onboarded'
    ACTIVE = 'active'
    INACTIVE = 'inactive'

    BUS_STATUS = (
        (ONBOARDED, 'onboarded'),
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
    )

    IN_PROGRESS = 'in_progress'
    INSTALLED = 'installed'
    NOT_INSTALLED = 'not_installed'
    FAULTY = 'faulty'
    LIVE = 'live'

    GPS_STATUS = (
        (IN_PROGRESS, 'in_progress'),
        (INSTALLED, 'installed'),
        (NOT_INSTALLED, 'not_installed'),
        (FAULTY, 'faulty'),
        (LIVE, 'live')
    )

    COMMISSION_VALIDATOR = [
        MaxValueValidator(30),
        MinValueValidator(0)
    ]

    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    BOOKING_OFF = 'booking_off'

    ONLINE_APP_BOOKING_COMMISSION = (
        (PERCENTAGE, 'percentage'),
        (FIXED, 'fixed'),
        (BOOKING_OFF, 'booking_off'),
    )

    FULL_AMOUNT = 'full_amount'

    QR_BOOKING_COMMISSION = (
        (FULL_AMOUNT, 'full_amount'),
        (BOOKING_OFF, 'booking_off')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    number = models.CharField(max_length=255, unique=True)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='related_bus', null=True)
    category = models.CharField(max_length=255, choices=BUS_CATEGORY, default=GENERAL)
    brand = models.CharField(max_length=255, null=True)
    has_wifi = models.BooleanField(default=False)
    has_power_plug = models.BooleanField(default=False)
    is_sanitized = models.BooleanField(default=False)
    is_air_conditioned = models.BooleanField(default=False)
    operating_as = models.CharField(max_length=255, null=True, blank=True)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    driver_contact = models.CharField(max_length=20, null=True, blank=True)
    conductor_name = models.CharField(max_length=255, null=True, blank=True)
    conductor_contact = models.CharField(max_length=20, null=True, blank=True)
    seat_type = models.CharField(max_length=50, choices=SEAT_TYPE)
    layout_type = models.CharField(max_length=255, choices=LAYOUT_TYPES, default=LAYOUT_1)
    is_multi_axle = models.BooleanField(default=False)
    normal_seats_capacity = models.PositiveIntegerField(default=0)
    single_sleeper_capacity = models.PositiveIntegerField(default=0)
    sharing_sleeper_capacity = models.PositiveIntegerField(default=0)
    upper_single_sleeper_capacity = models.PositiveIntegerField(default=0)
    upper_sharing_sleeper_capacity = models.PositiveIntegerField(default=0)
    recliner_capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=255, choices=BUS_STATUS, default=ONBOARDED)
    gps_status = models.CharField(max_length=255, choices=GPS_STATUS, default=NOT_INSTALLED)
    # deprecated
    commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    digital_commission = models.IntegerField(validators=COMMISSION_VALIDATOR)
    cash_commission = models.IntegerField(validators=COMMISSION_VALIDATOR)
    is_booking_allowed = models.BooleanField(default=True)
    is_qr_booking_allowed = models.BooleanField(default=True)
    is_pos_connected = models.BooleanField(default=True)
    printing_enabled = models.BooleanField(default=False)
    trips_access = models.BooleanField(default=True)
    print_bus_number = models.BooleanField(default=True)
    access_password = models.CharField(max_length=255, null=True, blank=True)
    ticket_header = models.CharField(max_length=255, null=True, blank=True)
    ticket_footer = models.CharField(max_length=255, default="ApniBus वॉलेट में ₹250 तक जीतें, नीचे दिए नंबर पर कॉल करें")
    subscription_pending = models.BooleanField(default=False)
    apply_concession = models.BooleanField(default=True)
    apply_bus_discount = models.BooleanField(default=False)
    apply_qr_discount = models.BooleanField(default=False)
    show_passenger_in_poc = models.BooleanField(default=True)

    online_app_booking_commission = models.CharField(max_length=255, choices=ONLINE_APP_BOOKING_COMMISSION, null=True, default=PERCENTAGE)
    qr_booking_commission = models.CharField(max_length=255, choices=QR_BOOKING_COMMISSION, null=True, default=FULL_AMOUNT)

    history = HistoricalRecords()
    is_ticket_amount_editable = models.BooleanField(default=False)
    is_show_seat_type = models.BooleanField(default=False)

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

