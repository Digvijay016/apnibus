import uuid
from django.db import models
from .user import User
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class SalesTeamUser(TimeStampedModel):

    SALES = 'sales'
    MARKETING = 'marketing'

    TYPE = (
        (SALES, 'sales'),
        (MARKETING, 'marketing'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='internal_team_user', null=True)
    name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    type = models.CharField(max_length=255, choices=TYPE, default=SALES)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mobile}"

    @staticmethod
    @receiver(post_save, sender='account.SalesTeamUser')
    def post_save_callback(sender, instance,created, **kwargs):
        if created:
            mobile_number = instance.mobile
            name = instance.name
            internal_user_obj, created = SalesTeamUser.objects.get_or_create(
                mobile=mobile_number, name=name, type=SalesTeamUser.SALES)

            if created:
                user = User.objects.create(
                    username=uuid.uuid1(), user_type=User.SALES)
                token = Token.objects.create(user=user)
                print('################',token)
                internal_user_obj.user = user
            internal_user_obj.save()
            instance.save()
        # print("################ 1",instance.route)
