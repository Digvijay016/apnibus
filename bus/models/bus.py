import uuid
from django.db import models
from account.models.operators import Operator
from account.views.aws_s3 import UploadAssetsToS3View
from utils.models import TimeStampedModel
from account.models.operators import Operator
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bus(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    operator = models.ForeignKey(
        Operator, on_delete=models.CASCADE, blank=True)
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
            pos_serial_img = instance.pos_serial_no
            gps_sim_img = instance.gps_sim_image

            upload_view = UploadAssetsToS3View()

            pos_serial_link, _ = upload_view.create(
                pos_serial_img, 'bus/' + instance.bus_number
            )
            gps_sim_link, _ = upload_view.create(
                gps_sim_img, 'bus/' + instance.bus_number
            )

            instance.pos_serial_no = pos_serial_link
            instance.gps_sim_image = gps_sim_link
            instance.save()
