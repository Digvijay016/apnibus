import uuid
from django.db import models
from .user import User
from utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class SalesTeamUser(AbstractUser, TimeStampedModel):

    SALES = 'sales'
    MARKETING = 'marketing'

    TYPE = (
        (SALES, 'sales'),
        (MARKETING, 'marketing'),
    )

    def save(self, *args, **kwargs):
        if not self.user:
            # Create the associated user if it doesn't exist
            self.user = User.objects.create(
                username=uuid.uuid1(), user_type=User.SALES)

        super().save(*args, **kwargs)

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sales_team_user_FK', null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=TYPE, default=SALES)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mobile}"

    @staticmethod
    @receiver(post_save, sender='account.SalesTeamUser')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            internal_user_obj = SalesTeamUser.objects.get(
                mobile=instance.mobile, type=SalesTeamUser.SALES)
            print('################', internal_user_obj)
            if internal_user_obj:
                token = Token.objects.create(user=internal_user_obj.user)
                print('################', token)
            instance.save()
