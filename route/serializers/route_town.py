from rest_framework import serializers
from route.models.route_town import RouteTown

class RouteTownSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteTown
        fields = ('id', 'route', 'town')
