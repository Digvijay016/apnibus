from bus.pagination import LocationListPagination
from rest_framework import generics
from rest_framework import status
from utils.restful_response import send_response
# from route.helpers.nearby_stoppages_data import final_nearby_townstoppages_data
from ..serializers import TownStoppageSerializer, TownStoppageResponseSerializer
from route.models import Town, TownStoppage
from utils.exception_handler import get_object_or_json404
from route.models import Route, RouteTown, RouteTownStoppage, ViaRoute, ViaRouteBasePricing
from bus.models import BusRouteTownStoppage, BusRouteTownStoppageJourney
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from utils.date_time_utils import difference_in_days


class CreateTownStoppageView(generics.CreateAPIView):
    """
    working: Using this API to create town stoppage
    """

    serializer_class = TownStoppageSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        town_id = request.data.get('town_id', None)
        town = get_object_or_json404(Town.objects.all(), id=town_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name_translation = request.data.get('name_translation', None)
            if name_translation:
                hindi_name = name_translation.get('hindi', None)

                if hindi_name:
                    instance = serializer.save(hindi_name=hindi_name)
            instance = serializer.save(town=town)
            data = self.get_serializer(instance).data
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class TownStoppageSearchView(generics.ListAPIView):
    """
    working: Using this API to list town stoppages.
    """
    queryset = TownStoppage.objects.all()
    serializer_class = TownStoppageResponseSerializer
    pagination_class = LocationListPagination

    def list(self, request, *args, **kwargs):
        """
        :param request: town_id(Optional)
        :param request: name(Required) - Will filtered the queryset to return town_Stoppages which contains passed name
        in their name field.
        :return: list of town_stoppages.
        """
        queryset = self.queryset
        town_id = request.GET.get('town_id', None)
        name = request.GET.get('name')
        is_paginated = request.GET.get('is_paginated', False)

        if town_id:
            queryset = queryset.filter(town_id=town_id)

        queryset = queryset.filter(name__icontains=name).order_by('name')

        if is_paginated:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)

        else:
            serializer = self.get_serializer(queryset, many=True)

        data = serializer.data

        if is_paginated:
            data = self.get_paginated_response(data).data

        # data = self.get_serializer(queryset, many=True).data
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)


class NearByTownStoppageSearchView(generics.ListAPIView):
    serializer_class = TownStoppageResponseSerializer

    def list(self, request, *args, **kwargs):

        lat = request.GET.get('latitude', None)
        long = request.GET.get('longitude', None)
        lat = float(lat)
        long = float(long)

        # for approx 1 KM distance 0.01 value add in latitude or longitude
        # for example latitude is same and we add 0.01 in longitude than distance between both location is approx 1.1 KM

        value = 0.01

        max_lat = lat + value
        max_long = long + value

        min_lat = lat - value
        min_long = long - value

        queryset = TownStoppage.objects.filter(latitude__lt=max_lat, longitude__lt=max_long,
                                               latitude__gt=min_lat, longitude__gt=min_long).exclude(latitude=lat, longitude=long)

        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data

        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)


class TownStoppageUpdateView(generics.UpdateAPIView):
    """
    working: Using this API to update town stoppage info.
    """

    serializer_class = TownStoppageSerializer
    queryset = TownStoppage.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        town = self.get_object()
        serializer = self.get_serializer(town, data=request.data, partial=True)
        if serializer.is_valid():
            name_translation = request.data.get('name_translation', None)
            if name_translation:
                hindi_name = name_translation.get('hindi', None)
                if hindi_name:
                    instance = serializer.save(hindi_name=hindi_name)
            instance = serializer.save()
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.', data=serializer.data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class DeleteTownStoppageView(generics.DestroyAPIView):
    """
    working: Using this API to delete town_stoppage and other depended entries in other tables.
    """
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        town_stoppage_id = request.GET.get('town_stoppage_id')
        town_stoppage_obj = TownStoppage.objects.get(id=town_stoppage_id)
        route_town_stoppages = RouteTownStoppage.objects.filter(
            town_stoppage=town_stoppage_obj)

        bus_route_town_stoppages = BusRouteTownStoppage.objects.filter(
            route_town_stoppage__in=route_town_stoppages)
        bus_route_town_stoppage_journeys = BusRouteTownStoppageJourney.objects.filter(
            bus_route_town_stoppage__in=bus_route_town_stoppages)

        bus_route_town_stoppage_journeys.delete()
        bus_route_town_stoppages.delete()
        town_stoppage_obj.delete()

        """
        Route
        RouteTown
        RouteTownStoppage
        ViaRoute
        ViaRouteBasePricing
        BusRoute
        BusRouteTown
        BusRouteTownStoppage
        BusRouteTownStoppageJourney
        BusRouteJourney
        BusViaRoute
        BusViaRouteJourney
        BusViaRouteJourneyPricing
        BusViaRoutePricing
        """
        return send_response(
            status=status.HTTP_200_OK,
            developer_message="Request was successful.",
            ui_message="Request was successful"
        )


class NearByPositionView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        try:
            town_stoppage_id = request.GET.get('town_stoppage_id', None)
            start_date = request.GET.get('start_date', None)
            end_date = request.GET.get('end_date', None)

            if not town_stoppage_id:
                return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="town_stoppage_id is missing")

            town_stoppage = TownStoppage.objects.get(id=town_stoppage_id)

            latitude = float(town_stoppage.latitude)
            longitude = float(town_stoppage.longitude)

            lat_range = [latitude - 0.01, latitude + 0.01]
            long_range = [longitude - 0.01, longitude + 0.01]

            if start_date and end_date:
                total_days, start_date_obj, end_date_obj = difference_in_days(
                    end_date, start_date)

                if total_days > 3 or total_days < 0:
                    return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="Invalid dates")

            data = final_nearby_townstoppages_data(
                lat_range, long_range, start_date, end_date)

            return send_response(status=status.HTTP_200_OK, data=data, developer_message="Request was successful")

        except Exception as ex:
            print(ex)

            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message=str(ex))
