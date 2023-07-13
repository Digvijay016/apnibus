from sqlite3 import Timestamp
from django.db import models

import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from account.models.sales_team import SalesTeamUser
from simple_history.models import HistoricalRecords
from account.views.aws_s3 import UploadAssetsToS3View
from utils.models import TimeStampedModel
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser


class Operator(models.Model):

    VERIFICATION_PENDING = 'p'
    VERIFIED = 'v'
    REJECTED = 'r'

    DEMO = 'd'
    SOLD = 's'

    POS_GIVEN_AS = (
        (DEMO, 'Demo'),
        (SOLD, 'Sold')
    )

    OPERATOR_STATUS = (
        (VERIFICATION_PENDING, 'Verification Pending'),
        (VERIFIED, 'Verified'),
        (REJECTED, 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)

    sales_user = models.ForeignKey(
        "account.SalesTeamUser", on_delete=models.CASCADE, related_name='operator_sales_user', null=True)
    
    name = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=255, blank=True, default="")
    gstin = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    pan_photo = models.ImageField(max_length=255, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, blank=True)
    aadhar_front_photo = models.ImageField(
        max_length=255, null=True, blank=True)
    aadhar_back_photo = models.ImageField(
        max_length=255, null=True, blank=True)
    setup_fee = models.IntegerField(blank=True)
    monthly_subscription_fee = models.IntegerField(blank=True)
    rejection_reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=225, choices=OPERATOR_STATUS, default=VERIFICATION_PENDING)
    pos_given_as = models.CharField(
        max_length=20, choices=POS_GIVEN_AS, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    @staticmethod
    @receiver(post_save, sender='account.Operator')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:

            adhar_front_link = ''
            adhar_back_link = ''
            pan_link = ''

            # Perform operations after creating a new instance
            if instance.aadhar_front_photo is not None:
                adhar_front_img = instance.aadhar_front_photo
            if instance.aadhar_back_photo is not None:
                adhar_back_img = instance.aadhar_back_photo
            if instance.pan_photo is not None:
                pan_img = instance.pan_photo

            upload_view = UploadAssetsToS3View()

            if adhar_front_img is not None and instance.mobile is not None:
                adhar_front_link, _ = upload_view.create(
                    adhar_front_img, 'operator/' + instance.mobile
                )
            if adhar_back_img is not None and instance.mobile is not None:
                adhar_back_link, _ = upload_view.create(
                    adhar_back_img, 'operator/' + instance.mobile
                )
            if pan_img is not None and instance.mobile is not None:
                pan_link, _ = upload_view.create(
                    pan_img, 'operator/' + instance.mobile
                )

            instance.aadhar_front_photo = adhar_front_link
            instance.aadhar_back_photo = adhar_back_link
            instance.pan_photo = pan_link
            instance.save()


