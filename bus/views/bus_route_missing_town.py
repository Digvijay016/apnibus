from rest_framework import viewsets

from bus.models.bus_route_missing_town import BusRouteMissingTown
from bus.serializers.bus_route_missing_town import BusRouteMissingTownSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class BusRouteMissingTownView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BusRouteMissingTown.objects.all()
    serializer_class = BusRouteMissingTownSerializer
