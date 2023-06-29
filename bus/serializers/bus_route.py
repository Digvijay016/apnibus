from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route import BusRoute
from route.serializers.route import RouteSerializer
from .bus import BusSerializer
# from rest_framework import serializers


class BusRouteSerializer(DynamicFieldsModelSerializer):
    # route = RouteSerializer(required=False)
    # bus = BusSerializer(required=False)

    class Meta:
        model = BusRoute
        fields = ('id', 'bus', 'from_town', 'to_town',
                  'start_time', 'arrival_time', 'route')

    # def get_remarks(self, obj):
    #     qs = OperatorRemark.objects.filter(bus_route=obj)
    #     serializer_data = OperatorRemarkSerializer(qs, many=True).data
    #     return serializer_data
