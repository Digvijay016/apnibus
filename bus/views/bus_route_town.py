from rest_framework import viewsets  # , generics, status
from bus.models.bus import Bus
from bus.models.bus_route_town import BusRouteTown
# from bus.models.bus_route import BusRoute
# from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
# from route.models.route_town import RouteTown
# from utils.restful_response import send_response
# from utils.exception_handler import get_object_or_json404
# , UpdateBusRouteTownSerializer, BusRouteTownResponseSerializer
from bus.serializers.bus_route_town import BusRouteTownSerializer
# from bus.pagination import BusListPagination
# from bus.helpers.bus_route_town import BusRouteTownUtils, update_day_in_bus_route_town
# from route.models.route_town_stoppage import RouteTownStoppage
# from utils.date_time_utils import get_time_from_duration
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusRouteTownView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRouteTown.objects.all()
    serializer_class = BusRouteTownSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']
    # lookup_field = 'bus_route_id'
