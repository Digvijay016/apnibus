from django.db import models

import uuid
from account.models.user import User
from simple_history.models import HistoricalRecords

from utils.models import TimeStampedModel


class Operator(TimeStampedModel):

    ONBOARDED = 'onboarded'
    DEBOARDED = 'deboarded'
    LOCKED = 'locked'


    OPERATOR_STATUS = (
        (ONBOARDED, 'onboarded'),
        (DEBOARDED, 'deboarded'),
        (LOCKED, 'locked'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator_user')
    name = models.CharField(max_length=255)
    hindi_name = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, unique=True)
    # email = models.EmailField(unique=True,null=True, default='abc@gmail.com')
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255, null=True, default="")
    gstin = models.CharField(max_length=20, null=True, blank=True)
    pan_number = models.CharField(max_length=20, null=True, blank=True)
    pan_photo = models.FileField(upload_to='operator/', null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    aadhar_front_photo = models.FileField(upload_to='operator/', null=True, blank=True)
    aadhar_back_photo = models.FileField(upload_to='operator/', null=True, blank=True)
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
    version = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=225, choices=OPERATOR_STATUS, default=ONBOARDED)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class OperatorBankAccount(TimeStampedModel):

    CURRENT = 'current'
    SAVING = 'saving'

    ACCOUNT_TYPE = (
        (CURRENT, 'current'),
        (SAVING, 'saving')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_holder_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)
    history = HistoricalRecords()


class OperatorPhotograph(TimeStampedModel):

    operator_photograph_id = models.UUIDField(default=uuid.uuid1, editable=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    photograph = models.FileField(upload_to='operator/', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.operator)