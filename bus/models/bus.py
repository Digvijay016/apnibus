import uuid
from django.db import models
from account.models.operators import Operator
from account.views.aws_s3 import UploadAssetsToS3View
from utils.models import TimeStampedModel
from account.models.operators import Operator
from simple_history.models import HistoricalRecords
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bus(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True)
    bus_number = models.CharField(max_length=255, unique=True)
    pos_serial_no = models.ImageField(max_length=255, null=True, blank=True)
    pos_dsn_number = models.CharField(max_length=255, null=True, blank=True)
    gps_sim_image = models.ImageField(max_length=255, null=True, blank=True)
    historical_records = HistoricalRecords()

    def __str__(self):
        return self.bus_number

    # @staticmethod
    # @receiver(pre_save, sender='account.Operator')
    # def pre_save_callback(sender, instance, **kwargs):
    #     # Check if the Operator instance already has a user
    #     if not instance.user_id:
    #         # Create a new User instance
    #         user = User.objects.create_user(
    #             username=str(instance.id),
    #             user_type=User.OPERATOR
    #         )
    #         # Assign the created User instance to the user field of Operator
    #         instance.user = user

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

            # print('############## ',pos_serial_link)
            # print('############## ',gps_sim_link)

            instance.pos_serial_no = pos_serial_link
            instance.gps_sim_image = gps_sim_link
            # instance.pan_photo = pan_link
            instance.save()


# class BusPhotograph(TimeStampedModel):
#     BUS_PHOTOGRAPH = 'bus_photograph'
#     RC = 'rc'

#     PHOTOGRAPH_TYPE = (
#         (BUS_PHOTOGRAPH, 'bus_photograph'),
#         (RC, 'rc')
#     )

#     bus_photograph_id = models.UUIDField(default=uuid.uuid1, editable=False)
#     bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
#     photograph = models.FileField(upload_to='bus/', null=True, blank=True)
#     description = models.TextField(null=True)
#     type = models.CharField(max_length=255, choices=PHOTOGRAPH_TYPE)
#     history = HistoricalRecords()

#     def __str__(self):
#         return self.id
