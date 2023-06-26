from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from pricing.models.price import PriceMatrix


class PriceSerializer(DynamicFieldsModelSerializer):
    # operator = OperatorSerializer(required=False)
    # remarks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PriceMatrix
        fields = ('id', 'bus_route', 'route_town',
                  'rows', 'columns', 'price_matrix')
