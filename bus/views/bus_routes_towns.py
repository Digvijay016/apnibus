import json
from rest_framework import viewsets, status
from bus.models.bus_routes_towns import BusRoutesTowns
from bus.serializers.bus_routes_towns import BusRoutesTownsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response


class CreateBusRoutesTownsView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRoutesTowns.objects.all()
    serializer_class = BusRoutesTownsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        route_id = self.request.query_params.get('route')
        if route_id:
            query_set = BusRoutesTowns.objects.filter(route=route_id)
            return query_set
        else:
            return self.queryset
