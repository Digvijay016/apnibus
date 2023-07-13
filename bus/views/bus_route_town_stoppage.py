from rest_framework import viewsets, generics, status
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from route.models.route_town_stoppage import RouteTownStoppage
from utils.restful_response import send_response
from utils.exception_handler import get_object_or_json404
from bus.serializers.bus_route_town_stoppage import BusRouteTownStoppageSerializer
from utils.date_time_utils import get_time_from_duration
from utils.apnibus_logger import apnibus_logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusRouteTownStoppageView(viewsets.ModelViewSet):
    """
    working: Using this to create BusRouteTownStoppage.
    """

    queryset = BusRouteTownStoppage.objects.all()
    serializer_class = BusRouteTownStoppageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
