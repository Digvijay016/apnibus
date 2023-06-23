from rest_framework import serializers
from route.models.district import District
from route.serializers.state import StateSerializer


class DistrictSerializer(serializers.ModelSerializer):

    state = StateSerializer(required=False)

    class Meta:
        model = District
        fields = ('id', 'name', 'hindi_name', 'state')
