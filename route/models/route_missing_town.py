import uuid
from django.db import models
from bus.models.bus_route import BusRoute
from utils.models import TimeStampedModel
from route.models.route import Route
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class RouteMissingTown(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True)
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, null=True, blank=True)
    missing_town = models.CharField(
        max_length=255, default='town', null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    history = HistoricalRecords()

    # @staticmethod
    # @receiver(post_save, sender='route.RouteMissingTown')
    # def post_save_callback(sender, instance, **kwargs):
    # print("################ 1",instance.route)
    # town, created = Town.objects.get_or_create(name=instance.missing_town)
    # if created:
    #     route_missing_town = RouteMissingTown.objects.create(town=town)
