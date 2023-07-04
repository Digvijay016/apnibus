from rest_framework import viewsets
from bus.models.bus_routes_towns import BusRoutesTowns
from bus.serializers.bus_routes_towns import BusRoutesTownsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusRoutesTownsView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRoutesTowns.objects.all()
    serializer_class = BusRoutesTownsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']
