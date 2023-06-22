from rest_framework import serializers
from route.models.route import Route
from bus.models.bus_route import BusRoute
# from location.serializers import TownSerializer
from utils.serializers import DynamicFieldsModelSerializer


class RouteSerializer(DynamicFieldsModelSerializer):
    # bus_count = serializers.SerializerMethodField()
    # town_count = serializers.SerializerMethodField()
    # from_town = TownSerializer(required=False)
    # to_town = TownSerializer(required=False)

    class Meta:
        model = Route
        fields = ('id', 'from_town', 'to_town', 'via', 'name')

    def get_bus_count(self, obj):
        return BusRoute.objects.filter(route=obj).count()

    # def get_town_count(self, obj):
    #     return RouteTown.objects.filter(route=obj).count()


class RouteSearchSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Route
        fields = ('id',  'name')

