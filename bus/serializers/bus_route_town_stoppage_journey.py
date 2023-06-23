from utils.serializers import DynamicFieldsModelSerializer
from bus.models import BusRouteTownStoppageJourney
from rest_framework import serializers
from account.models import User


class BusRouteTownStoppageJourneySerializer(DynamicFieldsModelSerializer):
    id = serializers.SerializerMethodField()
    stoppage_name = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    start_timestamp = serializers.SerializerMethodField()
    geofence_radius = serializers.SerializerMethodField()

    class Meta:
        model = BusRouteTownStoppageJourney
        fields = ('id', 'stoppage_name', 'start_time', 'start_timestamp', 'latitude', 'longitude', 'geofence_radius', 'geofence_status')

    def get_id(self, obj):
        id = obj.bus_route_town_stoppage.id
        return id

    def get_stoppage_name(self, obj):
        preferred_language = self.context.get('preferred_language', User.ENGLISH).lower()
        stoppage_obj = obj.bus_route_town_stoppage.route_town_stoppage.town_stoppage
        stoppage_name = stoppage_obj.name.capitalize()
        if preferred_language != User.ENGLISH.lower():
            stoppage_name = stoppage_obj.hindi_name
            if not stoppage_name:
                stoppage_name = stoppage_obj.name.capitalize()

        return stoppage_name

    def get_start_time(self, obj):
        start_time = obj.arrival_time.time()
        return start_time

    def get_start_timestamp(self, obj):
        start_timestamp = obj.arrival_time
        return start_timestamp

    def get_geofence_radius(self, obj):
        geofence_radius = obj.bus_route_town_stoppage.route_town_stoppage.town_stoppage.radius
        return geofence_radius

