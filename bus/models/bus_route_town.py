import uuid
from django.db import models
from bus.models.bus_route import BusRoute
from route.models.route import Route
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# import threading


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

    TODAY = 'Today'
    ALTERNATE = 'Alternate'

    RETURNCHOICES = (
        (TODAY, 'Today'),
        (ALTERNATE, 'Alternate')
    )

    YES = 'Yes'
    NO = 'No'

    ANOTHERTRIP = (
        (YES, 'Yes'),
        (NO, 'No')
    )

    # def save(self, *args, **kwargs):
    #     request = kwargs.pop('request', None)
    #     if request:
    #         # Access the request data
    #         data = request.data

    #         # Do something with the request data
    #         self.towns = data
    #     super().save(*args, **kwargs)

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, blank=True)
    towns = models.JSONField(default=list, blank=True)
    days = models.CharField(max_length=100, default='', choices=RETURNCHOICES)
    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, blank=True, related_name='bus_routes')
    another_trip = models.CharField(max_length=100, default='', choices=ANOTHERTRIP)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    # @staticmethod
    # @receiver(pre_save, sender='bus.BusRouteTown')
    # def pre_save_callback(sender, instance, **kwargs):

    #     request = threading.local().request
    #     if request:
    #         # Access the request data
    #         data = request.data
    #         # Do something with the request data
    #         # instance.field = data['field']
    #         print("############################################################")
    #         print(data)
    #         print("############################################################")
