from datetime import date
from rest_framework import status, generics
from utils.restful_response import send_response
# from bus.helpers.journey_extender import extend_journey_v2
from bus.models import BusRoute, BusRouteJourney
from bus.serializers import BusRouteJourneySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.date_time_utils import difference_in_days
# from bus.tasks import delete_wrong_journey_data


class ExtendBusRouteJourneys(generics.CreateAPIView):
    """
    working: Used for creating and extending journeys of buses.
    """

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        :param request: bus_route_id -  Bus route id for which user wants to create or extend journeys.
        :param request: start_date -  Start date of journeys.
        :param request: end_date -  End date of journeys.
        :return: Success response if user pass all required data otherwise will get failure.
        """
        bus_route_id = request.data.get('bus_route_id', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)

        today_date = str(date.today())

        # Added check on start date - Handled journeys creation in past
        total__diff_in_days, start_date_obj, end_date_obj = difference_in_days(
            today_date, start_date)

        if total__diff_in_days < -2:
            return send_response(
                status=status.HTTP_400_BAD_REQUEST,
                developer_message="Request Failed due to invalid data"
            )

        # Added check on end_date - Handled journeys creation for more than 30days
        total__diff_in_days, start_date_obj, end_date_obj = difference_in_days(
            today_date, end_date)

        if total__diff_in_days > 30:
            return send_response(
                status=status.HTTP_400_BAD_REQUEST,
                developer_message="Request Failed due to invalid data, End date should be less than 30days from today."
            )

        if bus_route_id and start_date and end_date:
            bus_route = BusRoute.objects.get(id=bus_route_id)
            # extend_journeys(bus_route, start_date, end_date)
            # extend_journey_v2(bus_route, start_date, end_date, auto=False)
            return send_response(
                status=status.HTTP_200_OK,
                developer_message="Request was successful.",
                ui_message="Request was successful.",
            )

        return send_response(
            status=status.HTTP_400_BAD_REQUEST,
            developer_message="Request was failed.",
            ui_message="Request was failed.",
        )


class BusRouteJourneyListView(generics.ListAPIView):
    """
    working: Used to view list of bus route journeys exists today and in future.
    """
    serializer_class = BusRouteJourneySerializer

    def list(self, request, *args, **kwargs):
        """
        :param request: bus_route_id - If bus route id is there then response will only contain journeys belongs to passes bus route.
        :param request: route_id - If route id is there then response will contain journeys of buses running on passes route.
        :param request: bus_number - If bus number is there then response will contain journeys of only this bus.
        :return: Desired list of bus route journeys.
        """
        bus_route_id = request.GET.get('bus_route_id', None)
        route_id = request.GET.get('route_id', None)
        bus_number = request.GET.get('bus_number', None)
        today_date = date.today()
        queryset = BusRouteJourney.objects.filter(start_time__gte=today_date)

        if bus_route_id:
            queryset = queryset.filter(bus_route_id=bus_route_id)

        if route_id:
            queryset = queryset.filter(bus_route__route_id=route_id)

        if bus_number:
            queryset = queryset.filter(bus_route__bus__number=bus_number)

        serializer = self.get_serializer(queryset, many=True)

        return send_response(
            status=status.HTTP_200_OK,
            developer_message="Request was successful.",
            ui_message="Request was successful.",
            data=serializer.data
        )


class BusRouteJourneyUpdateView(generics.UpdateAPIView):
    """
    working: Used to update details of bus route journey using id.
    """
    queryset = BusRouteJourney.objects.all()
    serializer_class = BusRouteJourneySerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_active = request.data.get('is_active', None)
        is_settled = request.data.get('is_settled', None)

        if str(is_active) != "None":
            instance.is_active = is_active

        if str(is_settled) != "None":
            instance.is_settled = is_settled

        instance.save()
        serializer = self.get_serializer(instance)

        return send_response(
            status=status.HTTP_200_OK,
            developer_message="Request was successful.",
            ui_message="Request was successful.",
            data=serializer.data
        )


class DeleteWrongJourneys(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        # delete_wrong_journey_data.delay()

        return send_response(status=status.HTTP_200_OK)
