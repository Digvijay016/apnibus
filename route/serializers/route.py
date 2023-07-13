from rest_framework import serializers
from route.models.route import Route
from bus.models.bus_route import BusRoute
from utils.serializers import DynamicFieldsModelSerializer


class RouteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'from_town', 'to_town', 'via', 'name')