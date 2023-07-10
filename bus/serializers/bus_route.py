# from bus.models.bus_route_return import BusRouteReturn
from bus.models.bus_routes_towns import BusRoutesTowns
from route.models.route import Route
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route import BusRoute
from route.serializers.route import RouteSerializer
from .bus import BusSerializer
from rest_framework import serializers


class BusRouteSerializer(DynamicFieldsModelSerializer):
    # route = RouteSerializer(required=False)
    # bus = BusSerializer(required=False)
    # towns = serializers.SerializerMethodField()

    class Meta:
        model = BusRoute
        fields = ('id', 'bus','route_selected' ,'from_town', 'to_town',
                  'start_time', 'arrival_time', 'return_id' ,'routes','towns')

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)

    #     request = self.context.get('request')
    #     print("###############################",request)

    #     # if request and request.method == 'GET':

    #     if representation['route_selected']:
            
    #         queryset = ''
    #         print("#########################",representation['return_id'])
    #         if not representation['return_id']:
    #             queryset = BusRoutesTowns.objects.filter(route=representation['route_selected'])
    #         else:
    #             queryset = BusRoute.objects.filter(id=representation['return_id'])
    #         print("###########################################",queryset)
    #         if queryset.exists():
    #             print("###############################",queryset)
    #             towns = queryset.values_list('towns', flat=True)
    #             print("###########################################")
    #             print(towns)
    #             towns = list(towns)[0]
    #             print("###########################################")
    #             towns = sorted(towns, key=lambda x:x['duration'])
    #             representation['towns'].append(towns)

    #     return representation

    # def get_towns(self, obj):
    #     print("##################################",obj)
    #     qs = BusRoutesTowns.objects.filter(route=obj)
    #     serializer_data = BusRoutesTowns(qs, many=True)
    #     print("##################################",serializer_data.data)
    #     return serializer_data.data

    # def get_remarks(self, obj):
    #     qs = OperatorRemark.objects.filter(bus_route=obj)
    #     serializer_data = OperatorRemarkSerializer(qs, many=True).data
    #     return serializer_data
