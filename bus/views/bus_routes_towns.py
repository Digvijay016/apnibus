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
    lookup_field = 'route'


    def get_queryset(self):
        route_id = self.request.query_params.get('route')
        if route_id:
            print("#######################",route_id)
            query_set = BusRoutesTowns.objects.filter(route=route_id)
            print("#######################",query_set)
            return query_set
        else:
            return self.queryset
