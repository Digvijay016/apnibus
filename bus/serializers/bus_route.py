from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route import BusRoute
from route.serializers.route import RouteSerializer
from .bus import BusSerializer
# from rest_framework import serializers


class BusRouteSerializer(DynamicFieldsModelSerializer):
    # route = RouteSerializer(required=False)
    # bus = BusSerializer(required=False, fields=('id', 'bus_number', 'pos_serial_no', 'pos_dsn_number', 'gps_sim_image'))

    class Meta:
        model = BusRoute
        fields = ('id','bus_number', 'from_town', 'to_town', 'departure_time', 'arrival_time')

    # def get_remarks(self, obj):
    #     qs = OperatorRemark.objects.filter(bus_route=obj)
    #     serializer_data = OperatorRemarkSerializer(qs, many=True).data
    #     return serializer_data