from http.client import responses
from rest_framework import viewsets
from bus.models.bus_route import BusRoute
from bus.serializers.bus_route import BusRouteSerializer
from bus.models.bus_route import BusRoute
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusRouteView(viewsets.ModelViewSet):
    """
    working: Used to create bus route.
    """

    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer

    # route_serializer = RouteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)