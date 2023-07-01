from rest_framework import viewsets #, generics, status
from bus.models.bus import Bus
from bus.models.bus_route_town import BusRouteTown
# from bus.models.bus_route import BusRoute
# from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
# from route.models.route_town import RouteTown
# from utils.restful_response import send_response
# from utils.exception_handler import get_object_or_json404
from bus.serializers.bus_route_town import BusRouteTownSerializer #, UpdateBusRouteTownSerializer, BusRouteTownResponseSerializer
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
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']
    # lookup_field = 'bus_route_id'

#     def create(self, request, *args, **kwargs):
#         """
#         :param request: bus_route_id - This is required to create bus route town
#         :param request: route_town_id - This is also required to create bus route town.
#         :return: BusRouteTown JSON object if passed data is valid otherwise returning error raised due to serializer failure.
#         """
#         # print("########### 1 ###########", request.data.pop('bus_route_id'))
#         # bus_route_id = request.data.pop('bus_route_id', None)
#         # route_town_id = request.data.pop('route_town_id', None)
#         # bus_route = get_object_or_json404(BusRoute.objects.all() , id=bus_route_id)
#         # route_town = get_object_or_json404(RouteTown.objects.all() , id=route_town_id)

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             # instance = serializer.save(
#             #     bus_route=bus_route, route_town=route_town)
#             instance = serializer.save()
#             # BusViaRouteUtils.create_bus_via_routes(instance.bus_route)
#             data = self.get_serializer(instance).data
#             return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#                                  data=data)

#         return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#                              ui_message='Invalid data', error=serializer.errors)


# class BusRouteTownListView(generics.ListAPIView):
#     """
#     working: Used to get list of bus route town.
#     """
#     serializer_class = BusRouteTownSerializer
#     queryset = BusRouteTown.objects.all()
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = (TokenAuthentication,)
#     pagination_class = BusListPagination

#     def list(self, request, *args, **kwargs):
#         """
#         :param request: bus_route_id(Optional) - If passed final list will contain bus route town of this bus route only.
#         :return: List of bus route towns.
#         """
#         # logic to send Bus routes? Filters?
#         queryset = self.queryset
#         bus_route_id = request.GET.get('bus_route_id', None)

#         if bus_route_id:
#             queryset = queryset.filter(bus_route_id=bus_route_id)

#         page = self.paginate_queryset(queryset)
#         serializer = self.get_serializer(page, many=True)
#         response = self.get_paginated_response(serializer.data)
#         return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#                              data=response.data)


# class UpdateBusRouteTownView(generics.UpdateAPIView):
#     """
#     working: Using this to update bus route town info.
#     """
#     queryset = BusRouteTown.objects.all()
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#     lookup_url_kwarg = 'id'
#     lookup_field = 'id'

#     def update(self, request, *args, **kwargs):
#         """
#         :param request: status(Optional) - Pass this if you want to update status of bus route town.
#         :param request: duration(Optional) - Pass this if you want to update duration of bus route town.
#         :return: If everything fine then will get updated BusRouteTown JSON object otherwise will get error info in response.
#         """

#         # Only duration and status update allowed
#         instance = self.get_object()
#         bus_route_town_status = request.data.get('status', None)
#         bus_route_town_eta_status = request.data.get('eta_status', None)
#         new_duration = request.data.get('duration', None)
#         tickets_count = 0
#         disable_tickets = False

#         if bus_route_town_eta_status:
#             instance.eta_status = bus_route_town_eta_status
#             instance.save()

#             if bus_route_town_eta_status == BusRouteTown.INACTIVE:
#                 bus_route_town_stoppages = BusRouteTownStoppage.objects.filter(
#                     bus_route_town=instance)
#                 bus_route_town_stoppages.update(
#                     eta_status=BusRouteTownStoppage.INACTIVE)

#             if bus_route_town_eta_status == BusRouteTown.ACTIVE:
#                 bus_route_town_stoppages = BusRouteTownStoppage.objects.filter(
#                     bus_route_town=instance)
#                 bus_route_town_stoppages.update(
#                     eta_status=BusRouteTownStoppage.ACTIVE)

#         if bus_route_town_status:
#             instance.status = bus_route_town_status
#             instance.save()

#             if bus_route_town_status == BusRouteTown.INACTIVE:
#                 tickets_count, disable_tickets = BusRouteTownUtils.disable_bus_route_town(
#                     bus_route_town=instance)

#             if bus_route_town_status == BusRouteTown.ACTIVE:
#                 BusRouteTownUtils.enable_bus_route_town(
#                     bus_route_town=instance)

#         if new_duration:
#             bus_route_towns_duration_list = BusRouteTown.objects.filter(bus_route=instance.bus_route).\
#                 order_by('duration').values_list('duration', flat=True)

#             try:
#                 bus_route_towns_duration_list = list(
#                     bus_route_towns_duration_list)
#                 sequence = bus_route_towns_duration_list.index(
#                     instance.duration)
#             except:
#                 return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#                                      ui_message='Invalid data')

#             if sequence == 0:
#                 return send_response(status=status.HTTP_400_BAD_REQUEST,
#                                      developer_message="Request failed. We can't update duration of first town.")

#             previous_route_town_duration = bus_route_towns_duration_list[sequence-1]

#             if sequence == len(bus_route_towns_duration_list) - 1:
#                 if previous_route_town_duration < new_duration:
#                     instance.duration = new_duration

#                 else:
#                     return send_response(status=status.HTTP_400_BAD_REQUEST,
#                                          developer_message="Last town duration should be greater than previous towns duration")

#             else:
#                 next_route_town_duration = bus_route_towns_duration_list[sequence+1]

#                 if not previous_route_town_duration < new_duration < next_route_town_duration:
#                     return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#                                          ui_message='BusRouteTown duration should be greater than previous town duration and '
#                                                     ' less than next ones respectively')
#                 instance.duration = new_duration

#             instance.save()
#         data = {}
#         if disable_tickets and tickets_count:
#             data = {
#                 'tickets_count': tickets_count
#             }
#             return send_response(status=status.HTTP_412_PRECONDITION_FAILED,
#                                  developer_message='Request was successful.',
#                                  data=data, ui_message=f"Tickets count - {tickets_count}")

#         return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.', data=data)


# class BusRouteTownMappingView(generics.CreateAPIView):
#     """
#     working: Using this API to map route towns and route town stoppages with bus route town and bus route town stoppages.
#     """
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)

#     def create(self, request, *args, **kwargs):
#         """
#         :param request: bus_route_id(required) - Pass bus route id for which you have to map route towns and route town stoppages with bus route town and bus route town stoppages.
#         :return: Created BusRouteTownStoppages JSON objects.
#         """
#         bus_route_id = request.data.get('bus_route_id', None)
#         bus_route = get_object_or_json404(
#             BusRoute.objects.all(), id=bus_route_id)
#         bus_route_start_time = bus_route.start_time

#         route_town_objs = RouteTown.objects.filter(
#             route=bus_route.route).order_by('duration')

#         for route_town_obj in route_town_objs.iterator():
#             bus_route_town, created = BusRouteTown.objects.get_or_create(
#                 bus_route=bus_route,
#                 route_town=route_town_obj
#             )
#             if created:
#                 bus_route_town.duration = route_town_obj.duration
#                 bus_route_town.save()

#             route_town_stoppages = RouteTownStoppage.objects.filter(
#                 route_town=route_town_obj).order_by('duration')

#             for route_town_stoppage in route_town_stoppages.iterator():
#                 bus_route_town_stoppage, created = BusRouteTownStoppage.objects.get_or_create(
#                     bus_route_town=bus_route_town,
#                     route_town_stoppage=route_town_stoppage
#                 )

#                 if created:
#                     bus_route_town_stoppage.duration = route_town_stoppage.duration
#                     bus_route_town_stoppage.latitude = route_town_stoppage.town_stoppage.latitude
#                     bus_route_town_stoppage.longitude = route_town_stoppage.town_stoppage.longitude

#                     total_duration = route_town_obj.duration + route_town_stoppage.duration
#                     bus_route_town_stoppage.start_time = get_time_from_duration(
#                         bus_route_start_time, total_duration)
#                     bus_route_town_stoppage.calculated_start_time = get_time_from_duration(
#                         bus_route_start_time, total_duration)
#                     bus_route_town_stoppage.save()

#         # Update day in bus route towns
#         update_day_in_bus_route_town(bus_route)

#         queryset = BusRouteTown.objects.filter(
#             bus_route=bus_route).order_by('duration')
#         serializer = BusRouteTownResponseSerializer(queryset, many=True)
#         return send_response(status=status.HTTP_200_OK, developer_message="Request was successful", data=serializer.data)
