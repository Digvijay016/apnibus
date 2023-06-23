from rest_framework import serializers
from route.models.route_town_stoppage import RouteTownStoppage
from route.serializers.town_stoppage import TownStoppageResponseSerializer


class RouteTownStoppageSerializer(serializers.ModelSerializer):
    town_stoppage = TownStoppageResponseSerializer(required=False)

    class Meta:
        model = RouteTownStoppage
        fields = ('id', 'route_town', 'town_stoppage', 'duration', 'status')
