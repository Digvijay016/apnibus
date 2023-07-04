from rest_framework import viewsets

from bus.models.bus_route_return import BusRouteReturn
from bus.serializers.bus_route_return import BusRouteReturnSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BusRouteReturnView(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BusRouteReturn.objects.all()
    serializer_class = BusRouteReturnSerializer
