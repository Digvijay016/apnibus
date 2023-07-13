from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage

class BusRouteTownSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = BusRouteTown
        fields = ('id', 'route', 'bus_route', 'towns','days','another_trip')