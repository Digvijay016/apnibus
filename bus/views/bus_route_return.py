from rest_framework import viewsets

from bus.models.bus_route_return import BusRouteReturn
from bus.serializers.bus_route_return import BusRouteReturnSerializer


class BusRouteReturnView(viewsets.ModelViewSet):

    queryset = BusRouteReturn.objects.all()
    serializer_class = BusRouteReturnSerializer
