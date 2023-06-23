from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models import BusRouteJourney


class BusRouteJourneySerializer(DynamicFieldsModelSerializer):
    bus_number = serializers.SerializerMethodField()
    route_name = serializers.SerializerMethodField()

    class Meta:
        model = BusRouteJourney
        fields = ('id', 'bus_route', 'bus_number', 'route_name', 'start_time', 'calculated_start_time', 'is_active',
                  'status', 'gps_status', 'calculated_start_time_type', 'is_settled')

    def get_bus_number(self, obj):
        return obj.bus_route.bus.number

    def get_route_name(self, obj):
        return obj.bus_route.route.name
