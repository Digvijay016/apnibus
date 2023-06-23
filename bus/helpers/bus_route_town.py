from django.db.models import Q
from utils.date_time_utils import find_time_diff_from_midnight
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus import Bus  # , BusViaRoute, BusViaRouteJourney, BusViaRouteJourneyPricing, BusViaRoutePricing, \
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage  # , BusRouteJourney
from bus.models.bus_route import BusRoute
# from bus.helpers.bus_via_route import BusViaRouteUtils
# from bus.helpers.bus_via_route_pricing import BusViaRoutePricingUtils
from datetime import date, datetime
# from bus.helpers.journey_extender import extend_bus_route_journey_v2


def update_day_in_bus_route_town(bus_route):
    bus_route_town_objs = BusRouteTown.objects.filter(
        bus_route=bus_route, status=BusRouteTown.ACTIVE).order_by('duration')

    route_day = 0
    bus_route_start_time = bus_route.start_time
    midnight_diff = find_time_diff_from_midnight(bus_route_start_time)

    for bus_route_town_obj in bus_route_town_objs.iterator():
        bus_route_town_duration = bus_route_town_obj.duration
        if bus_route_town_duration:
            if bus_route_town_duration >= midnight_diff:
                route_day = 1

        bus_route_town_obj.day = route_day
        bus_route_town_obj.save()


class BusRouteTownUtils():

    @classmethod
    def disable_bus_route_town(cls, bus_route_town):
        """
        param bus_route_town:
        return: None

        Ticket disable
        Delete bus via route journey pricing - Request for deletion
        Delete bus via route journey - Request for deletion
        Delete bus via route pricing - Request for deletion
        Delete bus via route - Request for deletion
        Delete bus route town - Request for deletion
        """

        tickets_count = 0
        disable_tickets = True
        # tickets_count = 0

        # bus_via_routes = BusViaRoute.objects.filter(
        #     Q(from_route_town=bus_route_town) | Q(to_route_town=bus_route_town)
        # )

        # bus_via_route_pricing_objs = BusViaRoutePricing.objects.filter(
        #     bus_via_route__in=bus_via_routes
        # )

        # bus_via_route_journey_objs = BusViaRouteJourney.objects.filter(
        #     bus_via_route__in=bus_via_routes
        # )

        # bus_via_route_journey_pricing_objs = BusViaRouteJourneyPricing.objects.filter(
        #     bus_via_route_journey__in=bus_via_route_journey_objs
        # )

        bus_route_town_stoppages = BusRouteTownStoppage.objects.filter(
            bus_route_town=bus_route_town)

        # if tickets_count == 0:
        #
        #     # Delete entries
        #     bus_route_town_stoppages.delete()
        #     bus_via_route_pricing_objs.delete()
        #     bus_via_route_journey_pricing_objs.delete()
        #     bus_via_route_journey_objs.delete()
        #     bus_via_routes.delete()
        #     bus_route_town.delete()
        #
        # else:

        # Update statuses
        bus_route_town_stoppages.update(status=BusRouteTownStoppage.INACTIVE)
        # bus_via_route_pricing_objs.update(status=BusViaRoutePricing.INACTIVE)
        # bus_via_route_journey_pricing_objs.update(
        #     status=BusViaRouteJourneyPricing.INACTIVE)
        # bus_via_route_journey_objs.update(status=BusViaRouteJourney.INACTIVE)
        # bus_via_routes.update(status=BusViaRoute.INACTIVE)

        return tickets_count, disable_tickets

    @classmethod
    def enable_bus_route_town(cls, bus_route_town):
        """
        param bus_route_town 
        return: None

        Generate bus via routes
        Generate via route pricing
        """""

        # Update status of bus route town stoppages
        BusRouteTownStoppage.objects.filter(bus_route_town=bus_route_town).update(
            status=BusRouteTownStoppage.ACTIVE)

        # # Generating bus via routes
        # BusViaRouteUtils.create_bus_via_routes_for_particular_town(
        #     bus_route_town=bus_route_town)

        # # Generating new bus via routes pricing
        # BusViaRoutePricingUtils.create_bus_via_route_pricing_for_particular_town(
        #     bus_route_town=bus_route_town)

        # Fix existing journeys
        time_now = datetime.now()
        # brjs = BusRouteJourney.objects.filter(
        #     bus_route=bus_route_town.bus_route, start_time__gte=time_now)
        # for brj in brjs:
        #     extend_bus_route_journey_v2.delay(brj.id)


def update_bus_route_towns_status():
    buses_obj = Bus.objects.filter(category=Bus.GENERAL)
    bus_routes_obj = BusRoute.objects.filter(bus__in=buses_obj)
    today_date = date.today()
    i = 1
    for bus_route_obj in bus_routes_obj:
        BusRouteTown.objects.filter(bus_route=bus_route_obj, status=BusRouteTown.INACTIVE).update(
            status=BusRouteTown.ACTIVE)
        BusRouteTownStoppage.objects.filter(bus_route_town__bus_route=bus_route_obj,
                                            status=BusRouteTownStoppage.INACTIVE).update(status=BusRouteTownStoppage.ACTIVE)
        # BusViaRouteUtils.create_bus_via_routes(bus_route_obj)
        # BusViaRoutePricingUtils.create_bus_via_route_pricing(bus_route_obj)
        # bus_via_route_journey_objs = BusViaRouteJourney.objects.filter(
        #     start_time__gte=today_date, bus_route_journey__bus_route=bus_route_obj, status=BusViaRouteJourney.INACTIVE)
        # for x in bus_via_route_journey_objs:
        #     BusViaRoutePricingUtils.create_bus_via_route_journey_pricing(x)

        i += 1
