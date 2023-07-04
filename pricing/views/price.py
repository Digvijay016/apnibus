from rest_framework import viewsets
from pricing.models.price import PriceMatrix
from pricing.serializers.price import PriceSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreatePriceView(viewsets.ModelViewSet):
    """
    working: Used for adding a bus.
    """

    # serializer_class = PriceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = PriceMatrix.objects.all()
    serializer_class = PriceSerializer

    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'bus_route_id'
