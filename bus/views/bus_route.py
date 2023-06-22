from rest_framework import generics, status
from bus.models.bus_route import BusRoute
from bus.serializers.bus_route import BusRouteSerializer
from utils.restful_response import send_response
from utils.exception_handler import get_object_or_json404
from bus.pagination import AdminBusListPagination, BusListPagination
# from route.models.route import Route
from bus.models.bus_route import BusRoute
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from bus.tasks import update_bus_via_route_journey_start_time, delete_bus_route
# from account.models import AdminUser
# from operators.helpers.remarks import add_remarks


class CreateBusRouteView(generics.CreateAPIView):
    """
    working: Used to create bus route.
    """

    serializer_class = BusRouteSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        :param request: route_id - Route on which we want to create bus_route.
        :param request: bus_id - Bus for which we want to create bus_route.
        :param request: start_time - Start time of bus.
        :return: BusRoute JSON object.
        """

        # route_id = request.data.pop('route_id')
        # bus_id = request.data.pop('bus_id')
        # start_time = request.data.get('start_time')
        # route = get_object_or_json404(Route.objects.all(), id=route_id)
        # bus = get_object_or_json404(Bus.objects.all(), id=bus_id)

        # if BusRoute.objects.filter(route=route, bus=bus, start_time__contains=start_time).exists():
        #     return send_response(status=status.HTTP_400_BAD_REQUEST, ui_message="Bus Route already exists",
        #                          developer_message="Bus Route already exists")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # instance = serializer.save(route=route, bus=bus, name=route.name)
            instance = serializer.save()

            # remarks = request.data.get('remarks', None)
            # if remarks:
            #     add_remarks(remarks, request.user.id, "BUS_ROUTE", bus_route_id=instance.id)

            data = self.get_serializer(instance).data
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class UpdateBusRouteView(generics.UpdateAPIView):
    """
    working: Used to update BusRoute info using his id.
    """

    serializer_class = BusRouteSerializer
    queryset = BusRoute.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        route = self.get_object()
        start_time = request.data.get('start_time', None)

        serializer = self.get_serializer(route, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()

            # Update start time in upcoming journeys
            if start_time:
                update_bus_via_route_journey_start_time.delay(instance.id, instance.start_time)

            remarks = request.data.get('remarks', None)
            if remarks:
                add_remarks(remarks, request.user.id, "BUS_ROUTE", bus_route_id=instance.id)

            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=serializer.data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class RouteDetailView(generics.RetrieveAPIView):
    """
    working: Used to retrieve info of a particular bus_route using his id.
    """

    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return send_response(response_code=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                 ui_message='The route_id you\'re trying to access does not exist')

        serializer = self.get_serializer(instance)
        return send_response(response_code=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=serializer.data)


class BusRouteListView(generics.ListAPIView):
    """
    working: Used to get list of bus routes in DB.
    """

    serializer_class = BusRouteSerializer
    queryset = BusRoute.objects.all()
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    pagination_class = AdminBusListPagination

    def list(self, request, *args, **kwargs):
        """
        :param request: bus_id - Pass bus_id in params if you want to get list of bus routes of a particular bus.
        :param request: route_id - Pass route_id in params if you want to get list of bus_routes of a particular route.
        :param request: bus_status - Pass bus_status in params if you want to get list of bus_routes of a particular bus_status.
        :return: List of targeted bus routes JSON objects.
        """

        # logic to send Bus routes? Filters?
        queryset = self.queryset
        bus_id = request.GET.get('bus_id', None)
        route_ids_list = request.GET.getlist('route_id', None)
        bus_status = request.GET.get('bus_status', None)

        if bus_id:
            queryset = queryset.filter(bus_id=bus_id)

        if route_ids_list:
            queryset = queryset.filter(route_id__in=route_ids_list)

        if bus_status:
            queryset = queryset.filter(bus__status=bus_status)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=response.data)


class DeleteBusRouteView(generics.DestroyAPIView):
    """
    working: Used to delete a particular bus_route using bus_route_id.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):

        bus_route_id = request.GET.get('bus_route_id')

        deleted_by = AdminUser.objects.filter(user=request.user).first()

        if deleted_by:
            deleted_by_name = deleted_by.display_name

            if not deleted_by_name:
                deleted_by_name = deleted_by.user.email

            delete_bus_route.delay(bus_route_id, deleted_by_name)

            return send_response(
                status=status.HTTP_200_OK,
                developer_message="Request was successful.",
                ui_message="Request was successful"
            )

        return send_response(
            status=status.HTTP_400_BAD_REQUEST,
            developer_message="Invalid User",
            ui_message="Invalid User"
        )
