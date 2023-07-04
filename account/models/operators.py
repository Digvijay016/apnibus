from django.db import models

import uuid
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from account.models.user import User
from simple_history.models import HistoricalRecords
from account.views.aws_s3 import UploadAssetsToS3View
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from utils.models import TimeStampedModel

class Operator(TimeStampedModel):

    VERIFICATIONPENDING = 'verification pending'
    VERIFIED = 'verified'
    ALL = 'all'
    REJECTED = 'rejected'

    DEMO = 'Demo'
    SOLD = 'Sold'

    POS_GIVEN_AS = (
        (DEMO, 'Demo'),
        (SOLD, 'Sold')
    )

    OPERATOR_STATUS = (
        (VERIFICATIONPENDING, 'verification pending'),
        (VERIFIED, 'verified'),
        (ALL, 'all'),
        (REJECTED, 'rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='operator_user')
    name = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=20, unique=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    town = models.CharField(max_length=255, blank=True, default="")
    gstin = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    pan_photo = models.ImageField(max_length=255, blank=True)
    aadhar_number = models.CharField(max_length=20, blank=True)
    aadhar_front_photo = models.ImageField(
        max_length=255, blank=True)
    aadhar_back_photo = models.ImageField(
        max_length=255, blank=True)
    setup_fee = models.IntegerField(blank=True)
    monthly_subscription_fee = models.IntegerField(blank=True)
    rejection_reason = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=225, choices=OPERATOR_STATUS, default=ALL)
    pos_given_as = models.CharField(
        max_length=20, choices=POS_GIVEN_AS, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.name)

    # def __str__(self):
    #     return self.id
    @staticmethod
    @receiver(pre_save, sender='account.Operator')
    def pre_save_callback(sender, instance, **kwargs):
        # Check if the Operator instance already has a user
        if not instance.user_id:
            # Create a new User instance
            user = User.objects.create_user(
                username=str(instance.id),
                user_type=User.OPERATOR
            )
            # Assign the created User instance to the user field of Operator
            instance.user = user
        uuid_value = uuid.uuid4()
        user = User.objects.create_user(
            username=uuid_value, user_type=User.OPERATOR)
        user.save()

        print("######### 1 ##########", user)

        token = Token.objects.create(user=user)
        print("######### 2 ##########", token)
        # token.save()

    @staticmethod
    @receiver(post_save, sender='account.Operator')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            # Perform operations after creating a new instance
            adhar_front_img = instance.aadhar_front_photo
            adhar_back_img = instance.aadhar_back_photo
            pan_img = instance.pan_photo

            upload_view = UploadAssetsToS3View()

            adhar_front_link, _ = upload_view.create(
                adhar_front_img, 'operator/' + instance.mobile
            )
            adhar_back_link, _ = upload_view.create(
                adhar_back_img, 'operator/' + instance.mobile
            )
            pan_link, _ = upload_view.create(
                pan_img, 'operator/' + instance.mobile
            )

            instance.aadhar_front_photo = adhar_front_link
            instance.aadhar_back_photo = adhar_back_link
            instance.pan_photo = pan_link
            instance.save()