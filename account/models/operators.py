# import operator
import os
import requests
from django.core.files import File
from django.db import models

import uuid
# from account.models.signals import pre_save_callback
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from account.models.user import User
from simple_history.models import HistoricalRecords
from account.views.aws_s3 import UploadAssetsToS3View
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from utils.models import TimeStampedModel
# from utils.aws_s3 import UploadFiles


# def s3_upload_path(instance, filename):
#     # Return the desired storage path in Amazon S3
#     # You can use the instance and filename to generate a unique path
#     # Example: 'path/to/s3/directory/filename.jpg'
#     # print(instance,"  ",filename)
#     # s3_url = instance.myfile.url
#     # # Remove the local development server URL prefix
#     # s3_url = s3_url.replace('http://localhost:8000/', '')
#     # print(s3_url)
#     return 'https://apnibus-bd-assets.s3.ap-south-1.amazonaws.com/bd_images/img/{}'.format(filename)


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

    # def s3_file_link(self,file_name):
    #     folder_name = settings.AWS_IMG_FOLDER
    #     file_link = UploadFiles.get_file_link(self,
    #         file_name=file_name, folder_name=folder_name)
    #     return file_link

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='operator_user')
    name = models.CharField(max_length=255,null=True)
    hindi_name = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=255,null=True)
    mobile = models.CharField(max_length=20, unique=True,null=True)
    # email = models.EmailField(unique=True,null=True, default='abc@gmail.com')
    address = models.CharField(max_length=255,null=True)
    town = models.CharField(max_length=255, null=True, default="")
    gstin = models.CharField(max_length=20, null=True, blank=True)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    pan_photo = models.ImageField(max_length=255, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    aadhar_front_photo = models.ImageField(
        max_length=255, null=True, blank=True)
    aadhar_back_photo = models.ImageField(
        max_length=255, null=True, blank=True)
    poc_name = models.CharField(max_length=20, null=True, blank=True)
    poc_number = models.CharField(max_length=20, null=True, blank=True)
    setup_fee = models.IntegerField(null=True, blank=True)
    monthly_subscription_fee = models.IntegerField(null=True, blank=True)
    bus_count = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    show_qr_code = models.BooleanField(default=True)
    show_ticket_msg = models.BooleanField(default=True)
    show_brand_name = models.BooleanField(default=True)
    show_mob_number = models.BooleanField(default=True)
    show_deductions = models.BooleanField(default=False)
    subscription_pending = models.BooleanField(default=False)
    rejection_reson = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=225, choices=OPERATOR_STATUS, default=ALL)
    pos_given_as = models.CharField(
        max_length=20, choices=POS_GIVEN_AS, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

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


# class OperatorBankAccount(TimeStampedModel):

#     CURRENT = 'current'
#     SAVING = 'saving'

#     ACCOUNT_TYPE = (
#         (CURRENT, 'current'),
#         (SAVING, 'saving')
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     operator = models.ForeignKey(
#         Operator, on_delete=models.CASCADE, related_name='bank_accounts')
#     bank_name = models.CharField(max_length=255, null=True, blank=True)
#     account_holder_name = models.CharField(
#         max_length=255, null=True, blank=True)
#     account_number = models.CharField(max_length=20, null=True, blank=True)
#     ifsc = models.CharField(max_length=20, null=True, blank=True)
#     account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
#     history = HistoricalRecords()


# class OperatorPhotograph(TimeStampedModel):

#     operator_photograph_id = models.UUIDField(
#         default=uuid.uuid1, editable=False)
#     operator = models.ForeignKey(
#         Operator, on_delete=models.CASCADE, null=True, blank=True)
#     type = models.CharField(max_length=255, null=True, blank=True)
#     photograph = models.FileField(upload_to='operator/', null=True, blank=True)
#     history = HistoricalRecords()

#     def __str__(self):
#         return str(self.operator)


# # def pre_save_callback(sender, instance, **kwargs):
# #     # Check if the Operator instance already has a user
# #     if not instance.user_id:
# #         # Create a new User instance
# #         user = User.objects.create_user(
# #             username=instance.id, user_type=User.OPERATOR)
# #         # Assign the created User instance to the user field of Operator
# #         instance.user = user


# # pre_save.connect(pre_save_callback, sender=Operator)


# # def post_save_callback(sender, instance, created, **kwargs):
# #     if created:
# #         # Perform operations after creating a new instance
# #         # aadhar_front_photo_value = instance.aadhar_front_photo
# #         # print('######### 1', aadhar_front_photo_value)
# #         # print('######### 2', created)
# #         adhar_front_img = instance.aadhar_front_photo
# #         adhar_back_img = instance.aadhar_back_photo
# #         pan_img = instance.pan_photo
# #         adhar_front_link, _ = UploadAssetsToS3View.create(adhar_front_img, 'operator/'+instance.mobile)
# #         adhar_back_link, _ = UploadAssetsToS3View.create(adhar_back_img,'operator/'+instance.mobile)
# #         pan_link, _ = UploadAssetsToS3View.create(pan_img,'operator/'+instance.mobile)

# #         instance.aadhar_front_photo = str(adhar_front_link)
# #         instance.aadhar_back_photo = str(adhar_back_link)
# #         instance.pan_photo = str(pan_link)
# #         instance.save()
# #     #     pass
# #     # else:
# #     #     # Perform operations after updating an existing instance
# #     #     pass


# # post_save.connect(post_save_callback, sender=Operator)
