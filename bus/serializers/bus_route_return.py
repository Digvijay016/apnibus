from bus.models.bus_route_return import BusRouteReturn
from utils.serializers import DynamicFieldsModelSerializer


class BusRouteReturnSerializer(DynamicFieldsModelSerializer):
    # bus_route = BusRouteSerializer(required=False, fields=('id',))
    # route_town = RouteTownSerializer(required=False, fields=('id', 'town'))
    # bus_route_town_stoppages = serializers.SerializerMethodField()

    class Meta:
        model = BusRouteReturn
        fields = ('id', 'route', 'bus', 'another_trip',
                  'from_town', 'to_town', 'start_time', 'arrival_time', 'days')  # , 'bus_route_town_stoppages')
