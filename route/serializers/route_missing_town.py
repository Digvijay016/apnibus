from rest_framework import serializers
from route.models.route_missing_town import RouteMissingTown
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage


class RouteMissingTownSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = RouteMissingTown
        fields = ('id', 'route', 'missing_town', 'duration')
