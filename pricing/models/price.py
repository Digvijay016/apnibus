# from email.policy import default
import uuid
from django.db import models

from bus.models.bus_route import BusRoute
from route.models.route_town import RouteTown
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from utils.exception_handler import get_object_or_json404


class PriceMatrix(models.Model):
    # name = models.CharField(max_length=100)
    # matrix = [[0 for _ in range(3)] for _ in range(3)]
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # bus_route = models.ForeignKey(
    #     BusRoute, on_delete=models.CASCADE, null=True)
    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, null=True)
    # route_town = models.ForeignKey(
    #     RouteTown, on_delete=models.CASCADE, null=True)
    # rows = models.PositiveIntegerField(default=3,null=True)
    # columns = models.PositiveIntegerField(default=3,null=True)
    price_matrix = models.JSONField(default=dict, null=True)
