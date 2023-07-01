import uuid
from django.db import models
from utils.models import TimeStampedModel
from route.models.route import Route
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class RouteMissingTown(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    missing_town = models.CharField(max_length=255,default='town', null=True)
    duration = models.IntegerField(null=True)
    history = HistoricalRecords()

    # @staticmethod
    # @receiver(post_save, sender='bus.BusMissingTown')
    # def post_save_callback(sender, instance, **kwargs):
    #     print("################ 1",instance.route)
