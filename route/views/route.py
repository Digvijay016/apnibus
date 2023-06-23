from rest_framework import generics, status
from route.serializers import RouteSerializer, RouteSearchSerializer
from utils.restful_response import send_response
from route.pagination import AdminRouteListPagination
from utils.exception_handler import get_object_or_json404
from route.models import Town
from route.models import Route, RouteTown, RouteTownStoppage, ViaRoute, ViaRouteBasePricing
from bus.models import BusRoute, BusRouteTown, BusRouteTownStoppage, BusViaRoute, BusViaRouteJourney, \
    BusRouteJourney, BusViaRoutePricing, BusViaRouteJourneyPricing, BusRouteTownStoppageJourney
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from route.helpers.route import clone_route, reverse_route


class CreateRouteView(generics.CreateAPIView):
    serializer_class = RouteSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        from_town_id = request.data.get('from_town_id')
        to_town_id = request.data.get('to_town_id')
        if serializer.is_valid():
            instance = serializer.save()
            from_town = get_object_or_json404(
                Town.objects.all(), id=from_town_id)
            to_town = get_object_or_json404(Town.objects.all(), id=to_town_id)
            name = from_town.name + "-" + to_town.name

            if instance.via:
                name += " via " + instance.via
            instance = serializer.save(
                from_town=from_town, to_town=to_town, name=name)
            data = self.get_serializer(instance).data
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class UpdateRouteView(generics.UpdateAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        from_town_id = request.data.get('from_town_id', None)
        to_town_id = request.data.get('to_town_id', None)
        via = request.data.get('via', None)

        if from_town_id:
            from_town = get_object_or_json404(
                Town.objects.all(), id=from_town_id)
            instance.from_town = from_town

        if to_town_id:
            to_town = get_object_or_json404(Town.objects.all(), id=to_town_id)
            instance.to_town = to_town

        if via:
            instance.via = via

        name = instance.from_town.name + " - " + \
            instance.to_town.name + " via " + instance.via
        instance.name = name
        instance.save()

        serializer = self.get_serializer(instance)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=serializer.data)


class RouteDetailView(generics.RetrieveAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    lookup_url_kwarg = 'id'
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                 ui_message='The route_id you\'re trying to access does not exist')

        serializer = self.get_serializer(instance)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=serializer.data)


class RouteListView(generics.ListAPIView):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    # pagination_class = AdminRouteListPagination

    def list(self, request, *args, **kwargs):
        # logic to send routes? Filters?
        route_id = request.GET.get('route_id', None)
        queryset = self.get_queryset()
        if route_id:
            queryset = queryset.filter(id=route_id)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=response.data)


class RouteSearchView(generics.ListAPIView):
    serializer_class = RouteSerializer

    def list(self, request, *args, **kwargs):
        name = request.GET.get('name')
        queryset = Route.objects.filter(name__icontains=name)
        data = self.get_serializer(queryset, many=True).data
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)


class RouteSearchViewAdminPanel(generics.ListAPIView):
    serializer_class = RouteSearchSerializer

    def list(self, request, *args, **kwargs):
        name = request.GET.get('name')
        queryset = Route.objects.filter(name__icontains=name)
        data = self.get_serializer(queryset, many=True).data
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)


class DeleteRouteView(generics.DestroyAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        route_id = request.GET.get('route_id')

        route_obj = Route.objects.get(id=route_id)
        route_towns = RouteTown.objects.filter(route=route_obj)
        route_town_stoppage = RouteTownStoppage.objects.filter(
            route_town__in=route_towns)

        bus_route = BusRoute.objects.filter(route=route_obj).first()
        bus_route_journeys = BusRouteJourney.objects.filter(
            bus_route=bus_route)
        bus_route_towns = BusRouteTown.objects.filter(bus_route=bus_route)
        bus_route_town_stoppages = BusRouteTownStoppage.objects.filter(
            bus_route_town__in=bus_route_towns)
        bus_route_town_stoppage_journeys = BusRouteTownStoppageJourney.objects.filter(
            bus_route_journey__in=bus_route_journeys)
        bus_via_routes = BusViaRoute.objects.filter(bus_route=bus_route)
        bus_via_route_journeys = BusViaRouteJourney.objects.filter(
            bus_route_journey__in=bus_route_journeys)
        bus_via_route_pricing = BusViaRoutePricing.objects.filter(
            bus_via_route__in=bus_via_routes)
        bus_via_route_journey_pricing = BusViaRouteJourneyPricing.objects.filter(
            bus_via_route_journey__in=bus_via_route_journeys)

        if bus_route:
            bus_via_route_journey_pricing.delete()
            bus_via_route_pricing.delete()
            bus_via_route_journeys.delete()
            bus_via_routes.delete()
            bus_route_town_stoppage_journeys.delete()
            bus_route_town_stoppages.delete()
            bus_route_towns.delete()
            bus_route_journeys.delete()
            bus_route.delete()

        route_town_stoppage.delete()
        route_towns.delete()
        route_obj.delete()

        return send_response(
            status=status.HTTP_200_OK,
            developer_message="Request was successful.",
            ui_message="Request was successful"
        )


class CloneRouteView(generics.CreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    serializer_class = RouteSerializer

    def create(self, request, *args, **kwargs):
        route_id = request.data.get("route_id")
        new_route_name = request.data.get("name", None)
        via = request.data.get("via", None)
        new_towns = request.data.get("new_towns", [])
        duration_from_first_town = request.data.get(
            "duration_from_first_town", 0)
        distance_from_first_town = request.data.get(
            "distance_from_first_town", 0)

        if not via:
            return send_response(
                status=status.HTTP_400_BAD_REQUEST,
                developer_message="Please add value of via",
                ui_message="Please add value of via"
            )

        try:
            new_route = clone_route(route_id, new_route_name, via, new_towns,
                                    duration_from_first_town, distance_from_first_town)

            data = self.get_serializer(new_route).data
            return send_response(
                status=status.HTTP_200_OK,
                data=data,
                developer_message="Request was successful.",
                ui_message="Request was successful"
            )

        except Exception as ex:
            return send_response(
                error={"message": str(ex)},
                status=status.HTTP_400_BAD_REQUEST,
                developer_message="Something went wrong",
                ui_message="Something went wrong",

            )


class ReverseRouteView(generics.CreateAPIView):
    serializer_class = RouteSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        route_id = request.data.get("route_id")

        # route_created, new_route = reverse_route(route_id)

        if route_created:
            serializer_data = self.get_serializer(new_route).data
            return send_response(
                status=status.HTTP_201_CREATED,
                data=serializer_data,
                developer_message="Request was successful",
                ui_message="Request was successful",
            )

        return send_response(
            status=status.HTTP_400_BAD_REQUEST,
            developer_message="Request failed",
            ui_message="Request failed",
        )
