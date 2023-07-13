# from email.policy import default
import uuid
from django.db import models

from bus.models.bus_route import BusRoute
from route.models.route_town import RouteTown
from utils.models import TimeStampedModel


class PriceMatrix(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    bus_route = models.ForeignKey(
        "bus.BusRoute", on_delete=models.CASCADE, blank=True)
    price_matrix = models.JSONField(default=list, blank=True)
