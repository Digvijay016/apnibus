# from django.utils import timezone
# import uuid
# from django.db import models
# from bus.models.bus_route import BusRoute
# from route.models.route_town import RouteTown
# from route.models.town import Town
# from utils.models import TimeStampedModel
# # from bus.models.bus_route import BusRoute
# from route.models.route import Route
# from simple_history.models import HistoricalRecords
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver


# class BusRouteReturn(TimeStampedModel):

#     TODAY = 'Today'
#     ALTERNATE = 'Alternate'

#     RETURNCHOICES = (
#         (TODAY, 'Today'),
#         (ALTERNATE, 'Alternate')
#     )

#     YES = 'Yes'
#     NO = 'No'

#     ANOTHERTRIP = (
#         (YES, 'Yes'),
#         (NO, 'No')
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     from_town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True)
#     to_town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True)
#     start_time = models.TimeField(default='00:00:00')
#     arrival_time = models.TimeField(default='00:00:00')
#     # route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True)
#     via = models.CharField(max_length=255, default='',blank=True)
#     days = models.CharField(max_length=100, default='', choices=RETURNCHOICES)
#     another_trip = models.CharField(
#         max_length=100, default='', choices=ANOTHERTRIP)
#     bus_route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, blank=True)
#     history = HistoricalRecords()

#     @staticmethod
#     @receiver(pre_save, sender='bus.BusRouteReturn')
#     def pre_save_callback(sender, instance, **kwargs):

#         # if Bus

#         from_town = Route.objects.filter(id=instance.route).values_list(
#             'to_town', flat=True).first()

#         # from_town_id = Town.objects.filter(
#         #     id=from_town)#.values_list('id', flat=True).first()

#         to_town = Route.objects.filter(id=instance.route).values_list(
#             'from_town', flat=True).first()

#         # to_town_id = Town.objects.filter(
#         #     id=to_town)#.values_list('id', flat=True).first()

#         # print("#########################",from_town)
#         # print("#########################",to_town)

#         instance.from_town_id = from_town
#         instance.to_town_id = to_town

#         # instance.save()
