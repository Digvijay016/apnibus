from rest_framework import serializers
from bus.models.bus_route_missing_town import BusRouteMissingTown
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage


class BusRouteMissingTownSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = BusRouteMissingTown
        fields = ('id', 'bus_route' ,'missing_town', 'duration')
