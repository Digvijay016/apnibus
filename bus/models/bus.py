import uuid
from django.db import models
from account.models.operators import Operator
from account.views.aws_s3 import UploadAssetsToS3View
from utils.models import TimeStampedModel
from route.models.town import Town
from account.models.operators import Operator
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class Bus(TimeStampedModel):

    SEATER = 'se'
    SLEEPER = 'sl'
    SEATER_SLEEPER = 'ss'
    UPPER_SINGLE_SLEEPER = 'usis'
    UPPER_SHARING_SLEEPER = 'ushs'
    RECLINER = 'r'

    SEAT_TYPE = (
        (SEATER, 'Seater'),
        (SLEEPER, 'Sleeper'),
        (SEATER_SLEEPER, 'Seater Sleeper'),
        (UPPER_SINGLE_SLEEPER, 'Upper Single Sleeper'),
        (UPPER_SHARING_SLEEPER, 'Upper Sharing Sleeper'),
        (RECLINER, 'Recliner')
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

    GENERAL = "g"
    EXPRESS = "e"
    LUXURY = "l"

    BUS_CATEGORY = (
        (GENERAL, "General"),
        (EXPRESS, "Express"),
        (LUXURY, "Luxury"),
    )

    ONBOARDED = 'o'
    ACTIVE = 'a'
    INACTIVE = 'i'

    BUS_STATUS = (
        (ONBOARDED, 'Onboarded'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    IN_PROGRESS = 'ip'
    INSTALLED = 'i'
    NOT_INSTALLED = 'ni'
    FAULTY = 'f'
    LIVE = 'l'

    GPS_STATUS = (
        (IN_PROGRESS, 'In Progress'),
        (INSTALLED, 'Installed'),
        (NOT_INSTALLED, 'Not Installed'),
        (FAULTY, 'Faulty'),
        (LIVE, 'Live')
    )

    COMMISSION_VALIDATOR = [
        MaxValueValidator(30),
        MinValueValidator(0)
    ]

    PERCENTAGE = 'p'
    FIXED = 'f'
    BOOKING_OFF = 'bo'

    ONLINE_APP_BOOKING_COMMISSION = (
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed'),
        (BOOKING_OFF, 'Booking Off'),
    )

    FULL_AMOUNT = 'f'

    QR_BOOKING_COMMISSION = (
        (FULL_AMOUNT, 'Full Amount'),
        (BOOKING_OFF, 'Booking Off')
    )


    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    operator = models.ForeignKey(
        Operator, on_delete=models.CASCADE, blank=True)
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
    seat_type = models.CharField(max_length=50, choices=SEAT_TYPE, default=SEATER)
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
    digital_commission = models.IntegerField(validators=COMMISSION_VALIDATOR,default=0)
    cash_commission = models.IntegerField(validators=COMMISSION_VALIDATOR, default=0)
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
    bus_number = models.CharField(max_length=255, unique=True, blank=True)
    pos_serial_no = models.ImageField(max_length=255, blank=True)
    pos_dsn_number = models.CharField(max_length=255, blank=True)
    gps_sim_image = models.ImageField(max_length=255, blank=True)
    historical_records = HistoricalRecords()

    def __str__(self):
        return str(self.bus_number)

    @staticmethod
    @receiver(post_save, sender='bus.Bus')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            # Perform operations after creating a new instance
            pos_serial_link = ''
            gps_sim_link = ''
            
            if instance.pos_serial_no:
                pos_serial_img = instance.pos_serial_no
            if instance.gps_sim_image:
                gps_sim_img = instance.gps_sim_image

            upload_view = UploadAssetsToS3View()

            if pos_serial_img and instance.bus_number:
                pos_serial_link, _ = upload_view.create(
                    pos_serial_img, 'bus/' + instance.bus_number
                )
            if gps_sim_img and instance.bus_number:
                gps_sim_link, _ = upload_view.create(
                    gps_sim_img, 'bus/' + instance.bus_number
                )

            instance.pos_serial_no = pos_serial_link
            instance.gps_sim_image = gps_sim_link
            instance.save()
