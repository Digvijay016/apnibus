from django.utils import timezone
import uuid
from django.db import models
from route.models.route_town import RouteTown
from route.models.town import Town
from utils.models import TimeStampedModel
from .bus import Bus
from route.models.route import Route
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class BusRoute(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    # bus_number = models.CharField(max_length=255, unique=True, default='APNI_BUS')
    from_town = models.CharField(max_length=255, default='from town')
    to_town = models.CharField(max_length=255, default='to town')
    start_time = models.TimeField(default='00:00:00')
    arrival_time = models.TimeField(default='00:00:00')
    route = models.JSONField(default=list, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.bus.number) + " --> " + str(self.from_town) + str(self.to_town) + str(self.departure_time) + str(self.arrival_time)

    def __str__(self):
        return str(self.id)

    @staticmethod
    @receiver(post_save, sender='bus.BusRoute')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            # Perform operations after creating a new instance
            # from_town_id = Town.objects.filter(name=instance.from_town).values_list('id', flat=True)
            # to_town_id = Town.objects.filter(name=instance.to_town).values_list('id', flat=True)

            queryset_from_town = Town.objects.filter(name=instance.from_town)
            uuid_route_from_town_id_list = [
                str(uuid) for uuid in queryset_from_town.values_list('id', flat=True)]

            queryset_to_town = Town.objects.filter(name=instance.to_town)
            uuid_route_to_town_id_list = [
                str(uuid) for uuid in queryset_to_town.values_list('id', flat=True)]
            # route [ {"route_id":"","route_name":"","via":""} ]
            print("############## from town id", uuid_route_from_town_id_list)
            print("############## to town id", uuid_route_to_town_id_list)

            route_id_from_town_list = RouteTown.objects.filter(
                town=uuid_route_from_town_id_list[0])
            uuid_route_from_town_route_id_list = [
                str(uuid) for uuid in route_id_from_town_list.values_list('route_id', flat=True)]

            route_id_to_town_list = RouteTown.objects.filter(
                town=uuid_route_to_town_id_list[0])
            uuid_route_to_town_route_id_list = [
                str(uuid) for uuid in route_id_to_town_list.values_list('route_id', flat=True)]

            for route_id in uuid_route_from_town_route_id_list:
                if route_id in uuid_route_to_town_route_id_list:
                    name = Route.objects.filter(id=route_id).values_list(
                        'name', flat=True).first()
                    via = Route.objects.filter(id=route_id).values_list(
                        'via', flat=True).first()
                    route_dict = {"route_id": route_id,
                                  "route_name": name, "via": via}
                    instance.route.append(route_dict)
                    # instance.via.append()

            print('############# from town route ids',
                  uuid_route_from_town_route_id_list)
            print('############# to town route ids',
                  uuid_route_to_town_route_id_list)
            instance.save()
