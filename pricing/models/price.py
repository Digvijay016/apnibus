from email.policy import default
import uuid
from django.db import models

from bus.models.bus_route import BusRoute
from route.models.route_town import RouteTown


class PriceMatrix(models.Model):
    # name = models.CharField(max_length=100)
    # matrix = [[0 for _ in range(3)] for _ in range(3)]
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # bus_route = models.ForeignKey(
    #     BusRoute, on_delete=models.CASCADE, null=True)
    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, null=False)
    # route_town = models.ForeignKey(
    #     RouteTown, on_delete=models.CASCADE, null=True)
    # rows = models.PositiveIntegerField(default=3,null=True)
    # columns = models.PositiveIntegerField(default=3,null=True)
    price_matrix = models.JSONField(default={}, null=True)
