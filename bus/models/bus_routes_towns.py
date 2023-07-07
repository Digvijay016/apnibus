import uuid
from django.db import models
from bus.models.bus_route_missing_town import BusRouteMissingTown
from route.models.route import Route
from route.models.town import Town
from route.models.route_town_stoppage import RouteTownStoppage
from route.models.town_stoppage import TownStoppage
from utils.models import TimeStampedModel
from route.models.route_town import RouteTown
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class BusRoutesTowns(TimeStampedModel):
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
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, blank=True)
    duration = models.IntegerField(blank=True)
    calculated_duration = models.IntegerField(blank=True)
    towns = models.JSONField(default=list, blank=True)
    day = models.IntegerField(blank=True, default=0)
    town_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    town_stoppage_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    eta_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)

    @staticmethod
    @receiver(post_save, sender='bus.BusRoutesTowns')
    def post_save_callback(sender, instance,created, **kwargs):
        if created:
            print("################ 1 ", instance.route)
            queryset = RouteTown.objects.filter(route=instance.route)
            uuid_town_id_list = [
                str(uuid) for uuid in queryset.values_list('town', flat=True)]

            route_town_ids_list = [
                str(uuid) for uuid in queryset.values_list('id', flat=True)]

            print("############## 2 ", route_town_ids_list)

            route_town_stoppage_list_qs = []

            for route_town_id in route_town_ids_list:
                query_set = RouteTownStoppage.objects.filter(
                    route_town=route_town_id)
                # print("########### 3 ", query_set)
                if query_set:
                    qs = query_set.values_list(
                        'town_stoppage', flat=True).order_by('duration')
                    route_town_stoppage_list_qs.append(qs)

            print("########### 3 ", route_town_stoppage_list_qs)

            route_town_stoppage_list = [
                str(uuid) for uuid in route_town_stoppage_list_qs[0].values_list('town_stoppage', flat=True)]

            print("############## 4 ", route_town_stoppage_list)

            town_stoppage_dict = {}
            town_stoppage_list = []
            for stoppage_id in route_town_stoppage_list:
                stoppage_name = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('name', flat=True).first()
                stoppage_town_id = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('town', flat=True).first()

                uuid_str = str(stoppage_town_id)

                town_stoppage_dict = {
                    'stoppage_id': stoppage_id,
                    'stoppage_name': stoppage_name,
                    'town_id': uuid_str
                }

                town_stoppage_list.append(town_stoppage_dict)

                print('############## 6 ', town_stoppage_dict)

            town_stoppage_list.append(town_stoppage_dict)
            print('############## 7 ', town_stoppage_list)

            for town_id in uuid_town_id_list:
                if town_id:
                    name = Town.objects.filter(id=town_id).values_list(
                        'name', flat=True).first()

                    duration = None

                    stoppage_list = []

                    for stoppage in town_stoppage_list:
                        if stoppage.get("town_id") == town_id:
                            stoppage_dct = {
                                "stoppage_id": stoppage.get("stoppage_id"),
                                "stoppage_name": stoppage.get("stoppage_name"),
                                "town_stoppage_status": instance.town_stoppage_status
                            }
                            stoppage_list.append(stoppage_dct)

                    if duration is None:
                        duration = 0

                    town_dict = {"town_id": town_id,
                                "town_name": name, "duration": duration, "town_status": instance.town_status, "stoppage": stoppage_list}  # , "via":via}

                    instance.towns.append(town_dict)

            missing_towns_queryset = BusRouteMissingTown.objects.all();

            missing_town_uuids = [
                str(uid) for uid in missing_towns_queryset.values_list('id',flat=True)
            ]

            for missing_town in missing_town_uuids:
                name = BusRouteMissingTown.objects.filter(id=missing_town).values_list('missing_town',flat=True).first()
                duration = BusRouteMissingTown.objects.filter(id=missing_town).values_list('duration',flat=True).first()

                dct = {
                    'town_id':missing_town,
                    'town_name': name,
                    'duration': duration,
                    'town_status':'inactive',
                    'stoppage':[]
                }

                print("#########################",dct)

                instance.towns.append(dct)   
            
            towns_lst = instance.towns
            print("############################################################")
            print(towns_lst)
            print("############################################################")
            towns_lst = sorted(towns_lst, key=lambda x: x['duration'])
            instance.towns.append(towns_lst[0])
            # instance.towns = sorted(instance.towns, key=lambda x: x['duration'])   
            instance.save()      