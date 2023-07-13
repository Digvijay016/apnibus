from rest_framework import serializers
from route.models.route_town_stoppage import RouteTownStoppage


class RouteTownStoppageSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTownStoppage
        fields = ('id', 'route_town', 'town_stoppage', 'duration', 'status')
