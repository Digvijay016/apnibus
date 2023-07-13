from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_routes_towns import BusRoutesTowns


class BusRoutesTownsSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = BusRoutesTowns
        fields = ('id', 'route', 'towns')
