from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
# from route.serializers. import RouteTownSerializer
from .bus_route import BusRouteSerializer
from .bus_route_town_stoppage import BusRouteTownStoppageResponseSerializer
# from route.serializers import TownSerializer
# , TownStoppageSerializer
# from route.models.route_town_stoppage import RouteTownStoppage
# from route.models.town_stoppage import TownStoppage


class BusRouteTownSerializer(DynamicFieldsModelSerializer):
    # bus_route = BusRouteSerializer(required=False, fields=('id',))
    # route_town = RouteTownSerializer(required=False, fields=('id', 'town'))
    bus_route_town_stoppages = serializers.SerializerMethodField()

    class Meta:
        model = BusRouteTown
        fields = ('id', 'bus_route', 'route_town',
                  'duration', 'status', 'eta_status','bus_route_town_stoppages')

    def get_bus_route_town_stoppages(self, obj):
        qs = BusRouteTownStoppage.objects.filter(
            bus_route_town=obj).order_by('duration')
        data = BusRouteTownStoppageResponseSerializer(qs, many=True).data
        return data


# class BusRouteTownResponseSerializer(DynamicFieldsModelSerializer):
#     # town = TownSerializer(source='route_town.town')
#     bus_route_town_stoppages = serializers.SerializerMethodField()

#     class Meta:
#         model = BusRouteTown
#         # fields = ('id', 'town', 'bus_route_town_stoppages',
#         #           'duration', 'status', 'eta_status')
#         fields = ('id', 'bus_route', 'route_town')

#     def get_bus_route_town_stoppages(self, obj):
#         from .bus_route_town_stoppage import BusRouteTownStoppageResponseSerializer
#         qs = BusRouteTownStoppage.objects.filter(
#             bus_route_town=obj).order_by('duration')
#         data = BusRouteTownStoppageResponseSerializer(qs, many=True).data
#         return data


# class UpdateBusRouteTownSerializer(DynamicFieldsModelSerializer):

#     status = serializers.MultipleChoiceField(
#         choices=[BusRouteTown.ACTIVE, BusRouteTown.INACTIVE], required=False)
#     duration = serializers.IntegerField(required=False)

#     class Meta:
#         model = BusRouteTown
#         fields = ('status', 'eta_status', 'duration')
