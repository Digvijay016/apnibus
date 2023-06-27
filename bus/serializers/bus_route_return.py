from rest_framework import serializers
from bus.models.bus_route_return import BusRouteReturn
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_return import BusRouteReturn


class BusRouteReturnSerializer(DynamicFieldsModelSerializer):
    # operator = OperatorSerializer(required=False)
    # remarks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BusRouteReturn
        fields = ('id', 'bus', 'route', 'from_town', 'to_town',
                  'start_time', 'arrival_time', 'route_return_type')
