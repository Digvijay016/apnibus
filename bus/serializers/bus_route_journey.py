# from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_journey import BusRouteJourney
from .bus import BusSerializer


class BusRouteJourneySerializer(DynamicFieldsModelSerializer):
    # bus_number = serializers.SerializerMethodField()
    # route_name = serializers.SerializerMethodField()

    bus = BusSerializer(required=False, fields=('id', 'bus_number', 'pos_serial_no', 'pos_dsn_number', 'gps_sim_image'))

    class Meta:
        model = BusRouteJourney
        fields = ('id', 'bus_route', 'bus_number', 'start_time', 'end_time')

    # def get_bus_number(self, obj):
    #     return obj.bus_route.bus.number
    #
    # def get_route_name(self, obj):
    #     return obj.bus_route.route.name
