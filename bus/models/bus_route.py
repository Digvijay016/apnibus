# from django.utils import timezone
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
    from_town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True, related_name='bus_route_from_town_FK')
    to_town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True, related_name='bus_route_to_town_FK')
    start_time = models.TimeField(default='00:00:00')
    arrival_time = models.TimeField(default='00:00:00')
    routes = models.JSONField(default=list, blank=True)
    towns = models.JSONField(default=list, blank=True)
    route_selected = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, blank=True)
    return_id = models.CharField(max_length=255, default='', blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    @staticmethod
    @receiver(post_save, sender='bus.BusRoute')
    def post_save_callback(sender, instance, created, **kwargs):
        if created:
            print("######################## Return Id",instance.return_id)
            queryset_from_town = Town.objects.filter(id=instance.from_town_id)
            uuid_route_from_town_id_list = [
                str(uuid) for uuid in queryset_from_town.values_list('id', flat=True)]

            queryset_to_town = Town.objects.filter(id=instance.to_town_id)
            uuid_route_to_town_id_list = [
                str(uuid) for uuid in queryset_to_town.values_list('id', flat=True)]

            print("############## from town id", uuid_route_from_town_id_list)
            print("############## to town id", uuid_route_to_town_id_list)

            if uuid_route_from_town_id_list:
                route_id_from_town_list = RouteTown.objects.filter(
                    town=uuid_route_from_town_id_list[0])
                uuid_route_from_town_route_id_list = [
                    str(uuid) for uuid in route_id_from_town_list.values_list('route_id', flat=True)]

                if uuid_route_to_town_id_list:
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
                            instance.routes.append(route_dict)
                            # instance.via.append()

                    print('############# from town route ids',
                        uuid_route_from_town_route_id_list)
                    print('############# to town route ids',
                        uuid_route_to_town_route_id_list)
            
            print("######################## Return Id",instance.return_id)
            if instance.return_id:
                qs = BusRoute.objects.filter(id=instance.return_id)
                instance.from_town_id = qs.values_list('to_town', flat=True).first()
                instance.to_town_id = qs.values_list('from_town', flat=True).first()
                qs_routes = qs.values_list('routes',flat=True)
                print("####################### Routes",qs_routes)
                instance.routes = []
                for route in qs_routes:
                    print("####################### Route",route)
                    if route:
                        for r in route:
                            r['route_name'] = ' '.join(r['route_name'].split(' ')[::-1])
                    instance.routes.append(route[0])

                from bus.models.bus_route_town import BusRouteTown
                queryset = BusRouteTown.objects.filter(bus_route=instance.return_id)
                towns = queryset.values_list('towns',flat=True)
                if towns:
                    # for town in towns:
                    towns_lst = towns[0]
                    length = len(towns_lst)-1
                    towns_lst = towns_lst[::-1]
                    print("##################################### Towns List")
                    print(towns_lst)
                    print("##################################### Towns List")
                    for i in range(0,length):
                        # print("########################### towns",i,towns_lst[i]['duration'],towns_lst[length-i-1]['duration'])
                        temp = towns_lst[i]['duration']
                        towns_lst[i]['duration'] = towns_lst[length-i-1]['duration']
                        towns_lst[length-i-1]['duration'] = temp
                        # break
                    instance.towns.append(towns_lst)

                route_selected = BusRoute.objects.filter(id=instance.return_id).values_list('route_selected',flat=True).first()
                bus_id = BusRoute.objects.filter(id=instance.return_id).values_list('bus',flat=True).first()

                instance.route_selected_id = route_selected
                instance.bus_id = bus_id
                print('#####################',route_selected, bus_id)
                    # instance.towns = sorted(instance.towns,key=lambda x:x['duration'])
            instance.save()
