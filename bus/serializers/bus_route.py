# from bus.models.bus_route_return import BusRouteReturn
from bus.models.bus_routes_towns import BusRoutesTowns
from route.models.route import Route
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route import BusRoute
from route.serializers.route import RouteSerializer
from .bus import BusSerializer
from rest_framework import serializers


class BusRouteSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = BusRoute
        fields = ('id', 'bus','route_selected' ,'from_town', 'to_town',
                  'start_time', 'arrival_time', 'return_id' ,'routes','towns')