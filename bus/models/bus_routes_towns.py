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


class BusRoutesTowns(models.Model):
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
    created_on = models.DateTimeField(auto_now_add=True, db_column='created_on')
    updated_on = models.DateTimeField(auto_now=True, db_column='updated_on')
    route = models.ForeignKey(
        "route.Route", on_delete=models.CASCADE, blank=True)
    towns = models.JSONField(default=list, blank=True)
    day = models.IntegerField(blank=True, default=0)
    town_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    town_stoppage_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id)


    @staticmethod
    @receiver(post_save, sender='bus.BusRoutesTowns')
    def post_save_callback(sender, instance,created, **kwargs):
        if created:
            queryset = RouteTown.objects.filter(route=instance.route)
            uuid_town_id_list = [
                str(uuid) for uuid in queryset.values_list('town', flat=True)]

            route_town_ids_list = [
                str(uuid) for uuid in queryset.values_list('id', flat=True)]

            route_town_stoppage_list_qs = []

            for route_town_id in route_town_ids_list:
                query_set = RouteTownStoppage.objects.filter(
                    route_town=route_town_id)
                if query_set:
                    qs = query_set.values_list(
                        'town_stoppage', flat=True).order_by('duration')
                    route_town_stoppage_list_qs.extend(qs)

            route_town_stoppage_list = [str(uuid) for uuid in route_town_stoppage_list_qs]

            town_stoppage_dict = {}
            town_stoppage_list = []
            for stoppage_id in route_town_stoppage_list:
                stoppage_name = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('name', flat=True).first()
                stoppage_town_id = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('town', flat=True).first()
                lattitude = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('latitude', flat=True).first()
                longitude = TownStoppage.objects.filter(
                    id=stoppage_id).values_list('longitude', flat=True).first()
                duration = RouteTownStoppage.objects.filter(town_stoppage=stoppage_id).values_list(
                        'duration', flat=True).first()
                uuid_str = str(stoppage_town_id)

                town_stoppage_dict = {
                    'stoppage_id': stoppage_id,
                    'stoppage_name': stoppage_name,
                    'town_id': uuid_str,
                    'lattitude': lattitude,
                    'longitude': longitude,
                    'duration' : duration
                }

                town_stoppage_list.append(town_stoppage_dict)

            town_stoppage_list.append(town_stoppage_dict)

            for town_id in uuid_town_id_list:
                if town_id:
                    name = Town.objects.filter(id=town_id).values_list(
                        'name', flat=True).first()

                    stoppage_list = []

                    for stoppage in town_stoppage_list:
                        if stoppage.get("town_id") == town_id:
                            stoppage_dct = {
                                "stoppage_id": stoppage.get("stoppage_id"),
                                "stoppage_name": stoppage.get("stoppage_name"),
                                "town_stoppage_status": instance.town_stoppage_status,
                                "lattitude" : stoppage.get("lattitude"),
                                "longitude" : stoppage.get("longitude"),
                                "duration" : stoppage.get("duration")
                            }
                            stoppage_list.append(stoppage_dct)

                    town_dict = {"town_id": town_id,
                                "town_name": name, "town_status": instance.town_status, "stoppage": stoppage_list}  # , "via":via}

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

                instance.towns.append(dct)   
            
            towns_lst = instance.towns
            towns_lst = sorted(towns_lst, key=lambda x: x['stoppage'][0]['duration'] if x['stoppage'] else float('inf'))
            instance.towns.append(towns_lst[0])  
            instance.save()  