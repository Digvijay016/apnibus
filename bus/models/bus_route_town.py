import uuid
from django.db import models
from bus.models.bus_route import BusRoute
from route.models.route import Route
from route.models.route_missing_town import RouteMissingTown
from route.models.town import Town
from route.models.route_town_stoppage import RouteTownStoppage
from route.models.town_stoppage import TownStoppage
# from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from utils.models import TimeStampedModel
# from bus.models.bus_route import BusRoute
from route.models.route_town import RouteTown
from simple_history.models import HistoricalRecords
# from .bus_route_town_stoppage import BusRouteTownStoppageResponseSerializer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# from rest_framework import serializers


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
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, null=True)
    duration = models.IntegerField(null=True)
    calculated_duration = models.IntegerField(null=True)
    missing_towns = models.JSONField(default=list, null=True)
    towns = models.JSONField(default=list, null=True)
    day = models.IntegerField(null=True, default=0)
    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, null=True, related_name='bus_routes')
    town_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    town_stoppage_status = models.CharField(
        max_length=20, choices=STATUS, default=ACTIVE)
    # status = models.CharField(
    #     max_length=20, choices=STATUS, default=ACTIVE)
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

    def __str__(self):
        return str(self.id)

    @staticmethod
    @receiver(pre_save, sender='bus.BusRouteTown')
    def pre_save_callback(sender, instance, **kwargs):
        # if created:

        #     instance.save()
        # bus_route_town_stoppages = instance.get_bus_route_town_stoppages()
        # print("################", bus_route_town_stoppages)
        print("################ 1 ", instance.route)
        queryset = RouteTown.objects.filter(route=instance.route)
        uuid_town_id_list = [
            str(uuid) for uuid in queryset.values_list('town', flat=True)]

        # town_stoppage_list = RouteTownStoppage.objects.values_list('town_stoppage', flat=True)

        route_town_ids_list = [
            str(uuid) for uuid in queryset.values_list('id', flat=True)]

        print("############## 2 ", route_town_ids_list)

        route_town_stoppage_list_qs = []

        missing_town_names = []

        missing_town_qs = RouteMissingTown.objects.filter(route=instance.route)

        missing_town_names = [
            str(name) for name in missing_town_qs.values_list('missing_town', flat=True)]

        print("Missing town names ###########", missing_town_names)

        instance.missing_towns = missing_town_names

        for route_town_id in route_town_ids_list:
            query_set = RouteTownStoppage.objects.filter(
                route_town=route_town_id)
            # print("########### 3 ", query_set)
            if query_set:
                qs = query_set.values_list('town_stoppage', flat=True).order_by('duration')
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

            # uuid_obj = uuid.UUID(stoppage_town_id)
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

                # duration = Town.objects.filter(id=town_id).values_list(
                #     'duration', flat=True).first()

                duration = None

                # boarding_points = []

                # town_stoppage_qs = RouteTownStoppage.objects.filter(town_stoppage=town_id).values_list(
                #     'town', flat=True)

                # uuid_town_stoppage_id_list = [
                #     str(uuid) for uuid in town_stoppage_list.values_list('town_stoppage', flat=True)]

                # for town_stoppage_id in uuid_town_stoppage_id_list:
                #     name = RouteTownStoppage.objects.filter(town=town_id).values_list(
                #         'name', flat=True).first()

                #     if name:
                #         boarding = {
                #             "town_stoppage_id": town_stoppage_id, "boarding_name": name}
                #         boarding_points.append(boarding)

                stoppage_list = []

                for stoppage in town_stoppage_list:
                    if stoppage.get("town_id") == town_id:
                        stoppage_dct = {
                            "stoppage_id": stoppage.get("stoppage_id"),
                            "stoppage_name": stoppage.get("stoppage_name"),
                            # "town_id": stoppage.get("town_id"),
                            "town_stoppage_status": instance.town_stoppage_status
                        }
                        stoppage_list.append(stoppage_dct)

                town_dict = {"town_id": town_id,
                             "town_name": name, "duration":duration ,"town_status": instance.town_status, "stoppage": stoppage_list}  # , "via":via}

                # town_dict['stoppage'] = town_stoppage_list
                instance.towns.append(town_dict)

    # def get_bus_route_town_stoppages(self, obj):
    #     qs = BusRouteTownStoppage.objects.filter(
    #         bus_route_town=obj).order_by('duration')
    #     data = BusRouteTownStoppageResponseSerializer(qs, many=True).data
    #     return data
