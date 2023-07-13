from rest_framework import serializers
from route.models.district import District
from route.serializers.state import StateSerializer


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('id', 'name', 'hindi_name', 'state',
                  'pincode', 'short_name', 'status')
