from rest_framework import serializers
from route.models.town import Town
from route.models.town_stoppage import TownStoppage
from route.serializers.district import DistrictSerializer
from utils.serializers import DynamicFieldsModelSerializer
from account.models.user import User


class TownSerializer(DynamicFieldsModelSerializer):

    district_name = serializers.CharField(
        source='district.name', read_only=True)

    class Meta:
        model = Town
        fields = ('id', 'name', 'district',
                  'status', 'district_name')
