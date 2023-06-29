from rest_framework import serializers
from route.models.route_town import RouteTown
# from route.serializers.town_stoppage import TownStoppageResponseSerializer


class RouteTownSerializer(serializers.ModelSerializer):
    # town_stoppage = TownStoppageResponseSerializer(required=False)

    class Meta:
        model = RouteTown
        fields = ('id', 'route', 'town')  # , 'duration', 'status')
