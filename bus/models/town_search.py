from email.policy import default
import uuid
from django.db import models
from route.models.district import District
from route.models.town import Town
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from django.db.models.signals import post_save
from django.dispatch import receiver


class TownSearch(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    towns = models.JSONField(default=list, null=True, blank=True)
    historical_records = HistoricalRecords()

    @staticmethod
    @receiver(post_save, sender='bus.TownSearch')
    def post_save_callback(instance, created, *args, **kwargs):
        if created:
            towns_qs = Town.objects.all()
            # district_qs = District.objects.all()

            towns_uids = [str(uid)
                          for uid in towns_qs.values_list('id', flat=True)]

            # district_uids = [str(uid) for uid in district_qs.values_list('district', flat=True)]

            # district_uids = list(set(district_uids))

            towns_lst = []
            towns_dct = dict()

            # district_town_ids = [str(uid)
            #               for uid in district_qs.values_list('town', flat=True)]

            # print("############### ", towns_uids)

            for town_id in towns_uids:
                town = Town.objects.filter(id=town_id)
                district = District.objects.filter(town=town_id)

                print("#################",town)
                print("#################",district)

                # district_id = town.values_list('district', flat=True).first()
                # if district_id in district_uids:
                town_name = town.values_list('name', flat=True).first()
                district_name = district.values_list('name', flat=True).first()        
                # towns_lst.append(town_name)
                if district_name not in towns_dct:
                    towns_dct[district_name] = []
                towns_dct[district_name].append(town_name)
            instance.towns.append(towns_dct)
            instance.save()
