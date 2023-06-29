import uuid
from django.db import models
# from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from utils.models import TimeStampedModel
from bus.models.bus_route import BusRoute
from route.models.route_town import RouteTown
from simple_history.models import HistoricalRecords
# from .bus_route_town_stoppage import BusRouteTownStoppageResponseSerializer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework import serializers


class BusRouteTown(TimeStampedModel):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    REQUEST_FOR_DELETION = 'request_for_deletion'
    DELETION_READY = 'deletion_ready'

    STATUS = (
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive'),
        (REQUEST_FOR_DELETION, 'request_for_deletion'),
        (DELETION_READY, 'deletion_ready')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, null=True)
    route_town = models.ForeignKey(
        RouteTown, on_delete=models.CASCADE, null=True)
    duration = models.IntegerField(null=True)
    calculated_duration = models.IntegerField(null=True)
    day = models.IntegerField(null=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default=ACTIVE)
    eta_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['bus_route', 'route_town'], name="UC_bus_route_route_town"),
    #     ]

    # def __str__(self):
    #     return str(self.bus_route) + "--" + str(self.route_town.town.name)

    # def __str__(self):
    #     return self.id

    @staticmethod
    @receiver(post_save, sender='bus.BusRouteTown')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            # bus_route_town_stoppages = instance.get_bus_route_town_stoppages()
            # print("################", bus_route_town_stoppages)
            print("################", instance.bus_route)

    # def get_bus_route_town_stoppages(self, obj):
    #     qs = BusRouteTownStoppage.objects.filter(
    #         bus_route_town=obj).order_by('duration')
    #     data = BusRouteTownStoppageResponseSerializer(qs, many=True).data
    #     return data
