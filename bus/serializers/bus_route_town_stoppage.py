from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from rest_framework import serializers
from account.models.user import User


class BusRouteTownStoppageSerializer(DynamicFieldsModelSerializer):
    # from .bus_route_town import BusRouteTownSerializer
    # from route.serializers.route_town_stoppage import RouteTownStoppageSerializer

    # bus_route_town = BusRouteTownSerializer(required=False)
    # route_town_stoppage = RouteTownStoppageSerializer(required=False)

    class Meta:
        model = BusRouteTownStoppage
        fields = (
            'id', 'bus_route_town', 'route_town_stoppage', 'latitude', 'longitude', 'duration', 'start_time',
            'is_active', 'status', 'eta_status')


# class BusRouteTownStoppageResponseSerializer(DynamicFieldsModelSerializer):
#     from route.serializers.route_town_stoppage import RouteTownStoppageSerializer

#     route_town_stoppage = RouteTownStoppageSerializer(required=False)

#     class Meta:
#         model = BusRouteTownStoppage
#         fields = (
#             'id', 'route_town_stoppage', 'latitude', 'longitude', 'duration', 'is_active', 'status', 'eta_status')


class BusRouteTownStoppageResponseSerializer(DynamicFieldsModelSerializer):
    stoppage_name = serializers.SerializerMethodField()

    class Meta:
        model = BusRouteTownStoppage
        fields = ('id', 'stoppage_name', 'duration',
                  'start_time', 'latitude', 'longitude')

    def get_stoppage_name(self, obj):
        preferred_language = self.context.get(
            'preferred_language', User.ENGLISH).lower()
        stoppage_obj = obj.route_town_stoppage.town_stoppage
        stoppage_name = stoppage_obj.name
        if preferred_language != User.ENGLISH.lower():
            stoppage_name = stoppage_obj.hindi_name
            if not stoppage_name:
                stoppage_name = stoppage_obj.name

        return stoppage_name
