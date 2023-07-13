from route.models.town_stoppage import TownStoppage
from route.serializers.town import TownSerializer
from utils.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers


class TownStoppageSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = TownStoppage
        fields = ('id', 'town', 'name', 'hindi_name', 'latitude', 'longitude', 'status', 'radius', 'type')