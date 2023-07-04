from rest_framework import serializers
from account.settings.base import BASE_DIR
from bus.models.town_search import TownSearch
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus import Bus


class TownSearchSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = TownSearch
        fields = ('id', 'towns')
