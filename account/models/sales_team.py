import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser, Group, Permission
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class SalesTeamUser(AbstractUser):

    SALES = 's'
    MARKETING = 'm'

    TEAM_TYPE = (
        (SALES, 'Sales'),
        (MARKETING, 'Marketing'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    created_on = models.DateTimeField(auto_now_add=True, db_column='created_on')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    otp = models.CharField(max_length=6, default=1234)
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10)
    team_type = models.CharField(max_length=255, choices=TEAM_TYPE, null=True ,default=SALES)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mobile}"

    @staticmethod
    @receiver(pre_save, sender='account.SalesTeamUser')
    def pre_save_callback(sender, instance, *args, **kwargs):
        instance.otp = get_random_string(length=4, allowed_chars='1234567890')
        instance.username = instance.mobile

    @staticmethod
    @receiver(post_save, sender='account.SalesTeamUser')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            Token.objects.create(user_id=instance.id)
