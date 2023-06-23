from route.models.town_stoppage import TownStoppage
from route.serializers.town import TownSerializer
from utils.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from account.models.user import User


class TownStoppageSerializer(DynamicFieldsModelSerializer):
    town = TownSerializer(required=False)
    # name_translation = serializers.SerializerMethodField(required=False)
    # radius = serializers.FloatField(required=False)

    class Meta:
        model = TownStoppage
        fields = ('id', 'town', 'name', 'hindi_name', 'latitude', 'longitude', 'status', 'name_translation', 'radius', 'type')

    def get_name_translation(self, obj):
        data = {
            'hindi': obj.hindi_name
        }
        return data


class TownStoppageResponseSerializer(DynamicFieldsModelSerializer):
    town = TownSerializer(required=False)
    # radius = serializers.FloatField(required=False)
    # name_translation = serializers.SerializerMethodField(required=False)
    # name = serializers.SerializerMethodField()

    class Meta:
        model = TownStoppage
        fields = ('id', 'town', 'name', 'hindi_name', 'latitude', 'longitude', 'status', 'name_translation', 'radius', 'type')

    def get_name(self, obj):
        context = self.context
        preferred_language = context.get('preferred_language', User.ENGLISH)
        if preferred_language.lower() == User.ENGLISH:
            name = obj.name
            name = name.replace("_", " ")
            name = name.split(" ")
            name = [p.capitalize() for p in name]
            name = " ".join(name)
            return name
        else:
            if obj.hindi_name:
                return obj.hindi_name
            else:
                return obj.name

    def get_name_translation(self, obj):
        data = {
            'hindi': obj.hindi_name
        }
        return data
