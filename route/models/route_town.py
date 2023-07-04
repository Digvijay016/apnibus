from django.db import models
from utils.models import TimeStampedModel
from route.models.town import Town
from route.models.route import Route
import uuid
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class RouteTown(TimeStampedModel):
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
        Route, on_delete=models.CASCADE, null=True, blank=True)
    town = models.ForeignKey(
        Town, on_delete=models.PROTECT, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['route', 'town'], name="UC_route_town")
        ]

    def __str__(self):
        return f"{self.route} + -> + {self.town.name}"

    # @staticmethod
    # @receiver(pre_save, sender='route.RouteTown')
    # def pre_save_callback(sender, instance, **kwargs):
    #     print("################ 1 ", instance.route)
    #     queryset = RouteTown.objects.filter(route=instance.route)
    #     uuid_town_id_list = [
    #         str(uuid) for uuid in queryset.values_list('town', flat=True)]

    #     route_town_ids_list = [
    #         str(uuid) for uuid in queryset.values_list('id', flat=True)]

    #     print("############## 2 ", route_town_ids_list)

    #     route_town_stoppage_list_qs = []

    #     for route_town_id in route_town_ids_list:
    #         query_set = RouteTownStoppage.objects.filter(
    #             route_town=route_town_id)
    #         if query_set:
    #             qs = query_set.values_list(
    #                 'town_stoppage', flat=True).order_by('duration')
    #             route_town_stoppage_list_qs.append(qs)

    #     print("########### 3 ", route_town_stoppage_list_qs)

    #     route_town_stoppage_list = [
    #         str(uuid) for uuid in route_town_stoppage_list_qs[0].values_list('town_stoppage', flat=True)]

    #     print("############## 4 ", route_town_stoppage_list)

    #     town_stoppage_dict = {}
    #     town_stoppage_list = []
    #     for stoppage_id in route_town_stoppage_list:
    #         stoppage_name = TownStoppage.objects.filter(
    #             id=stoppage_id).values_list('name', flat=True).first()
    #         stoppage_town_id = TownStoppage.objects.filter(
    #             id=stoppage_id).values_list('town', flat=True).first()

    #         uuid_str = str(stoppage_town_id)

    #         town_stoppage_dict = {
    #             'stoppage_id': stoppage_id,
    #             'stoppage_name': stoppage_name,
    #             'town_id': uuid_str
    #         }

    #         town_stoppage_list.append(town_stoppage_dict)

    #         print('############## 6 ', town_stoppage_dict)

    #     town_stoppage_list.append(town_stoppage_dict)
    #     print('############## 7 ', town_stoppage_list)

    #     for town_id in uuid_town_id_list:
    #         if town_id:
    #             name = Town.objects.filter(id=town_id).values_list(
    #                 'name', flat=True).first()

    #             duration = None

    #             stoppage_list = []

    #             for stoppage in town_stoppage_list:
    #                 if stoppage.get("town_id") == town_id:
    #                     stoppage_dct = {
    #                         "stoppage_id": stoppage.get("stoppage_id"),
    #                         "stoppage_name": stoppage.get("stoppage_name"),
    #                         "town_stoppage_status": instance.town_stoppage_status
    #                     }
    #                     stoppage_list.append(stoppage_dct)

    #             town_dict = {"town_id": town_id,
    #                          "town_name": name, "duration": duration, "town_status": instance.town_status, "stoppage": stoppage_list}  # , "via":via}

    #             instance.towns.append(town_dict)
