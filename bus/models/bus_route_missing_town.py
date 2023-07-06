import uuid
from django.db import models
# from route.models.route import Route
# from bus.models.bus_routes_towns import BusRoutesTowns
from utils.models import TimeStampedModel
from bus.models.bus_route import BusRoute
# from bus.models.bus_route_town import BusRouteTown
from simple_history.models import HistoricalRecords
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver


class BusRouteMissingTown(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True)
    # bus_route_generic = models.ForeignKey(
    #     BusRoutesTowns, on_delete=models.CASCADE, blank=True, related_name="bus_route_missing_town_FK")
    bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, null=True, blank=True)
    missing_town = models.CharField(
        max_length=255, default='town', blank=True)
    duration = models.IntegerField(blank=True)
    history = HistoricalRecords()

    # @staticmethod
    # @receiver(post_save, sender='route.RouteMissingTown')
    # def post_save_callback(sender, instance, **kwargs):
    # print("################ 1",instance.route)
    # town, created = Town.objects.get_or_create(name=instance.missing_town)
    # if created:
    #     route_missing_town = RouteMissingTown.objects.create(town=town)
