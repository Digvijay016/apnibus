from rest_framework import generics, status
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from route.models.route_town_stoppage import RouteTownStoppage
from utils.restful_response import send_response
from utils.exception_handler import get_object_or_json404
from bus.serializers.bus_route_town_stoppage import BusRouteTownStoppageSerializer
# from bus.helpers.bus_route_town_stoppage import BusRouteTownStoppageUtils
from utils.date_time_utils import get_time_from_duration
from utils.apnibus_logger import apnibus_logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateBusRouteTownStoppageView(generics.CreateAPIView):
    """
    working: Using this to create BusRouteTownStoppage.
    """

    queryset = BusRouteTownStoppage.objects.all()
    serializer_class = BusRouteTownStoppageSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

#     def create(self, request, *args, **kwargs):
#         """
#         :param request: bus_route_town_id(required)
#         :param request: route_town_stoppage_id(required)
#         :return: BusRouteTownStoppage JSON object if passed data is valid otherwise will return errors raised by serializer.
#         """

#         bus_route_town_id = request.data.get('bus_route_town_id', None)
#         route_town_stoppage_id = request.data.get(
#             'route_town_stoppage_id', None)
#         bus_route_town = get_object_or_json404(
#             BusRouteTown.objects.all(), id=bus_route_town_id)
#         route_town_stoppage = get_object_or_json404(
#             RouteTownStoppage.objects.all(), id=route_town_stoppage_id)

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             bus_route = bus_route_town.bus_route
#             bus_route_start_time = bus_route.start_time
#             total_duration = bus_route_town.duration + \
#                 request.data.get('duration')
#             bus_route_town_stoppage_start_time = get_time_from_duration(
#                 bus_route_start_time, total_duration)

#             instance = serializer.save(
#                 bus_route_town=bus_route_town,
#                 route_town_stoppage=route_town_stoppage,
#                 start_time=bus_route_town_stoppage_start_time
#             )
#             data = self.get_serializer(instance).data
#             return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#                                  data=data)

#         return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#                              ui_message='Invalid data', error=serializer.errors)


# class BusRouteTownStoppageListView(generics.ListAPIView):
#     """
#     working: Can use this to get list of bus route town stoppages list.
#     """
#     serializer_class = BusRouteTownStoppageSerializer
#     queryset = BusRouteTownStoppage.objects.all()
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = (TokenAuthentication,)
#     # pagination_class = BusListPagination

#     def list(self, request, *args, **kwargs):
#         """
#         :param request: bus_route_id(Optional) - If bus_route_id is there then response will contain stoppages of passes bus route only.
#         :param request: bus_id(Optional) - If bus_id is there then response will contain stoppages of passes bus only.
#         :return: List of filtered bus route town stoppages JSON objects.
#         """
#         queryset = self.queryset
#         bus_route_id = request.GET.get('bus_route_id', None)
#         bus_id = request.GET.get('bus_id', None)

#         if bus_route_id:
#             queryset = queryset.filter(
#                 bus_route_town__bus_route_id=bus_route_id)

#         if bus_id:
#             queryset = queryset.filter(
#                 bus_route_town__bus_route__bus_id=bus_id)
#         serializer = self.get_serializer(queryset, many=True)
#         return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#                              data=serializer.data)


# class BusUpdateRouteTownStoppageView(generics.UpdateAPIView):
#     """
#     working: API to update BusRouteTownStoppage
#     """
#     serializer_class = BusRouteTownStoppageSerializer
#     queryset = BusRouteTownStoppage.objects.all()
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#     lookup_url_kwarg = 'id'
#     lookup_field = 'id'

#     # def update(self, request, *args, **kwargs):
#     #     bus_route_town_stoppage = self.get_object()
#     #     new_duration = request.data.get('duration', None)
#     #     bus_route_town_stoppage_status = request.data.get('status', None)
#     #     latitude = request.data.get('latitude', None)
#     #     longitude = request.data.get('longitude', None)
#     #     serializer = self.get_serializer(
#     #         bus_route_town_stoppage, data=request.data, partial=True)
#     #     tickets_count = 0
#     #     disable_tickets = False

#     #     if serializer.is_valid():
#     #         if not bus_route_town_stoppage_status and not new_duration:
#     #             if latitude:
#     #                 bus_route_town_stoppage.latitude = latitude

#     #             if longitude:
#     #                 bus_route_town_stoppage.longitude = longitude

#     #             bus_route_town_stoppage.save()
#     #             instance = serializer.save()

#     #             return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#     #                                  data=serializer.data)

#     #         else:
#     #             if bus_route_town_stoppage_status:
#     #                 bus_route_town_stoppage.status = bus_route_town_stoppage_status
#     #                 bus_route_town_stoppage.save()

#     #                 if bus_route_town_stoppage_status == BusRouteTownStoppage.INACTIVE:
#     #                     tickets_count, disable_tickets = BusRouteTownStoppageUtils.disable_bus_route_town_stoppage(
#     #                         bus_route_town_stoppage)

#     #                 if bus_route_town_stoppage_status == BusRouteTownStoppage.ACTIVE:
#     #                     BusRouteTownStoppageUtils.enable_bus_route_town_stoppage(
#     #                         bus_route_town_stoppage)

#     #                 elif bus_route_town_stoppage_status == BusRouteTownStoppage.DELETION_READY:
#     #                     BusRouteTownStoppageUtils.delete_bus_route_town_stoppage(
#     #                         bus_route_town_stoppage)

#     #             if new_duration:
#     #                 bus_route_town_stoppages_list = BusRouteTownStoppage.objects.filter(
#     #                     bus_route_town=bus_route_town_stoppage.bus_route_town
#     #                 ).order_by('duration').values_list('duration', flat=True)

#     #                 try:
#     #                     bus_route_town_stoppages_list = list(
#     #                         bus_route_town_stoppages_list)
#     #                     sequence = bus_route_town_stoppages_list.index(
#     #                         bus_route_town_stoppage.duration)
#     #                 except Exception as ex:
#     #                     apnibus_logger.error(ex)
#     #                     return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#     #                                          ui_message='Invalid data')

#     #                 if sequence == 0:
#     #                     return send_response(status=status.HTTP_400_BAD_REQUEST,
#     #                                          developer_message="Request failed. We can't update duration "
#     #                                                            "of first route town stoppage.")

#     #                 previous_route_town_duration = bus_route_town_stoppages_list[sequence - 1]
#     #                 if sequence == len(bus_route_town_stoppages_list) - 1:
#     #                     if previous_route_town_duration < new_duration:
#     #                         bus_route_town_stoppage.duration = new_duration

#     #                     else:
#     #                         return send_response(status=status.HTTP_400_BAD_REQUEST,
#     #                                              developer_message="Last RouteTownStoppage duration should be greater "
#     #                                                                "than previous RouteTownStoppage duration")

#     #                 else:
#     #                     next_route_town_duration = bus_route_town_stoppages_list[sequence + 1]
#     #                     if not previous_route_town_duration < new_duration < next_route_town_duration:
#     #                         return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#     #                                              ui_message='RouteTownStoppage duration should be greater than previous '
#     #                                                         'RouteTownStoppage duration and less than next ones '
#     #                                                         'respectively')

#     #                     bus_route_town_stoppage.duration = new_duration

#     #             data = {}
#     #             if disable_tickets and tickets_count:
#     #                 data.update({
#     #                     'tickets_count': tickets_count
#     #                 })
#     #                 return send_response(status=status.HTTP_412_PRECONDITION_FAILED, developer_message='Request was successful.',
#     #                                      data=data, ui_message=f"Tickets count - {tickets_count}")

#     #         return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#     #                              data=data)

#     #     else:
#     #         apnibus_logger.error(serializer.errors)
#     #         return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
#     #                              ui_message='Invalid data', error=serializer.errors)
