from rest_framework import serializers
from route.models.town import Town
from route.models.town_stoppage import TownStoppage
from route.serializers.district import DistrictSerializer
from utils.serializers import DynamicFieldsModelSerializer
from account.models.user import User


class TownSerializer(DynamicFieldsModelSerializer):
    # district = DistrictSerializer(required=False)
    # town_stoppage_count = serializers.SerializerMethodField(required=False)
    # name_translation = serializers.SerializerMethodField(required=False)
    # name = serializers.SerializerMethodField()

    class Meta:
        model = Town
        fields = ('id', 'name', 'district',
                  'status', 'type')

#     def get_name(self, obj):
#         context = self.context
#         name = obj.name
#         preferred_language = context.get('preferred_language', User.ENGLISH)
#         if preferred_language.lower() == User.ENGLISH:
#             name = name.replace("_", " ")
#             name = name.split(" ")
#             name = [p.capitalize() for p in name]
#             name = " ".join(name)
#             return name
#         else:
#             return obj.hindi_name

#     def get_town_stoppage_count(self, obj):
#         return TownStoppage.objects.filter(town=obj).count()

#     def get_name_translation(self, obj):
#         data = {
#             'hindi': obj.hindi_name
#         }
#         return data


# class CreateTownSerializer(DynamicFieldsModelSerializer):
#     district = DistrictSerializer(required=False)
#     town_stoppage_count = serializers.SerializerMethodField(required=False)
#     name_translation = serializers.SerializerMethodField(required=False)

#     class Meta:
#         model = Town
#         fields = ('id', 'name', 'district', 'town_stoppage_count',
#                   'status', 'name_translation', 'type')

#     def get_town_stoppage_count(self, obj):
#         return TownStoppage.objects.filter(town=obj).count()

#     def get_name_translation(self, obj):
#         data = {
#             'hindi': obj.hindi_name
#         }
#         return data
