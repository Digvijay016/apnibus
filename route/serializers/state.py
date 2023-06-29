from rest_framework import serializers
from route.models.state import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name', 'code', 'short_name', 'hindi_name')
