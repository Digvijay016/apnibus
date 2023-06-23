from rest_framework import generics, status
from route.models import RouteTown, RouteTownStoppage
from route.serializers import RouteTownStoppageSerializer
from utils.restful_response import send_response
from utils.exception_handler import get_object_or_json404
from location.models import TownStoppage
from route.models import RouteTownStoppage
from route.helpers.route_town_stoppage import RouteTownStoppageUtils
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from route.tasks import create_route_town_stoppage


class CreateRouteTownStoppageView(generics.CreateAPIView):

    serializer_class = RouteTownStoppageSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        route_town_id = request.data.get('route_town_id')
        town_stoppage_id = request.data.get('town_stoppage_id')
        route_town = get_object_or_json404(
            RouteTown.objects.all(), id=route_town_id)
        town_stoppage = get_object_or_json404(
            TownStoppage.objects.all(), id=town_stoppage_id)

        if RouteTownStoppage.objects.filter(route_town=route_town, town_stoppage=town_stoppage).exists():
            return send_response(status=status.HTTP_400_BAD_REQUEST, ui_message="Route town Stoppage already exists",
                                 developer_message="Route town Stoppage already exists")

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(
                route_town=route_town, town_stoppage=town_stoppage)
            data = self.get_serializer(instance).data

            # Utility to perform sync after object creation
            create_route_town_stoppage(instance.id)
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class UpdateRouteTownStoppageView(generics.UpdateAPIView):

    serializer_class = RouteTownStoppageSerializer
    queryset = RouteTownStoppage.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        route_town_stoppage = self.get_object()
        new_duration = request.data.get('duration', None)
        route_town_stoppage_status = request.data.get('status', None)
        serializer = self.get_serializer(
            route_town_stoppage, data=request.data, partial=True)
        tickets_count = 0
        disable_tickets = False

        if route_town_stoppage_status:
            route_town_stoppage.status = route_town_stoppage_status
            route_town_stoppage.save()

            if route_town_stoppage_status == RouteTownStoppage.INACTIVE:
                tickets_count, disable_tickets = RouteTownStoppageUtils.disable_route_town_stoppage(
                    route_town_stoppage)

            # elif route_town_stoppage_status == RouteTownStoppage.ACTIVE:
            #     RouteTownStoppageUtils.enable_route_town_stoppage(route_town_stoppage)

            elif route_town_stoppage_status == RouteTownStoppage.DELETION_READY:
                RouteTownStoppageUtils.delete_route_town_stoppage(
                    route_town_stoppage)

        if new_duration:
            route_town_stoppages_list = RouteTownStoppage.objects.filter(
                route_town=route_town_stoppage.route_town
            ).order_by('duration').values_list('duration', flat=True)

            try:
                route_towns_stoppage_list = list(route_town_stoppages_list)
                sequence = route_towns_stoppage_list.index(
                    route_town_stoppage.duration)
            except Exception as ex:
                return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                     ui_message='Invalid data')

            if sequence == 0:
                return send_response(status=status.HTTP_400_BAD_REQUEST,
                                     developer_message="Request failed. We can't update duration "
                                                       "of first route town stoppage.")

            previous_route_town_stoppage_duration = route_town_stoppages_list[sequence - 1]
            if sequence == len(route_town_stoppages_list) - 1:
                if previous_route_town_stoppage_duration < new_duration:
                    route_town_stoppage.duration = new_duration

                else:
                    return send_response(status=status.HTTP_400_BAD_REQUEST,
                                         developer_message="Last RouteTownStoppage duration should be greater "
                                                           "than previous RouteTownStoppage duration")

            else:
                next_route_town_stoppage_duration = route_towns_stoppage_list[sequence + 1]
                if not previous_route_town_stoppage_duration < new_duration < next_route_town_stoppage_duration:
                    return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                         ui_message='RouteTownStoppage duration should be greater than previous '
                                                    'RouteTownStoppage duration and less than next ones '
                                                    'respectively')

                route_town_stoppage.duration = new_duration

        if serializer.is_valid():
            if not route_town_stoppage_status and not new_duration:
                instance = serializer.save()

                return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                     data=instance.data)

            else:
                data = {}
                if disable_tickets and tickets_count:
                    data.update({
                        'tickets_count': tickets_count
                    })

                    return send_response(status=status.HTTP_412_PRECONDITION_FAILED,
                                         developer_message='Request was successful.',
                                         data=data, ui_message=f"Tickets count - {tickets_count}")

                return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                     data=data)

        else:
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                 ui_message='Invalid data', error=serializer.errors)


class RouteTownStoppageDetailView(generics.RetrieveAPIView):

    queryset = RouteTownStoppage.objects.all()
    serializer_class = RouteTownStoppageSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                 ui_message='The route_town_stoppage_id you\'re trying to access does not exist')

        serializer = self.get_serializer(instance)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=serializer.data)


class RouteTownStoppageListView(generics.ListAPIView):
    serializer_class = RouteTownStoppageSerializer
    queryset = RouteTownStoppage.objects.all()
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    # pagination_class = RouteListPagination

    def list(self, request, *args, **kwargs):
        route_town_id = request.GET.get('route_town_id')
        queryset = RouteTownStoppage.objects.filter(
            route_town_id=route_town_id).order_by('duration')
        serializer = self.get_serializer(queryset, many=True)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=serializer.data)
