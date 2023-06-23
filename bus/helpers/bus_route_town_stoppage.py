from datetime import datetime
from bus.helpers.bus_route_town_stoppage_journey import create_single_bus_route_town_stoppage_journey
from bus.models.bus_route_town_stoppage import  BusRouteTownStoppage
from bus.models.bus_route_town_stoppage_journey import  BusRouteTownStoppageJourney
# from bus.models import  BusRouteJourney
from utils.date_time_utils import get_time_from_duration
# from booking.models import TicketDetail, Ticket
# from bus.helpers.bus_route_town_stoppage_journey import create_single_bus_route_town_stoppage_journey


class BusRouteTownStoppageUtils():

    @classmethod
    def disable_bus_route_town_stoppage(cls, bus_route_town_stoppage):
        # Ticketing
        disable_tickets = True

        # ticket_detail_objs = TicketDetail.objects.filter(boarding_point=bus_route_town_stoppage)
        # tickets_count = ticket_detail_objs.count()

        # if tickets_count:
        #     ticket_ids = ticket_detail_objs.values_list("ticket_id", flat=True)

        #     tickets = Ticket.objects.filter(id__in=ticket_ids)

        #     # Update tickets status
        #     tickets.update(status=Ticket.CANCELLED_BY_APNIBUS)

        brtsjs = BusRouteTownStoppageJourney.objects.filter(
            bus_route_town_stoppage=bus_route_town_stoppage)

        # Delete BusRouteTownStoppageJourney or if we want to update status of BusRouteTownStoppageJourney then
        # we need to add status field in model.

        # if not tickets_count:
        brtsjs.delete()

        # return tickets_count, disable_tickets
        return disable_tickets

    @classmethod
    def enable_bus_route_town_stoppage(cls, bus_route_town_stoppage):
        time_now = datetime.now()

        # Upcoming bus route journeys
        brjs = BusRouteJourney.objects.filter(bus_route=bus_route_town_stoppage.bus_route_town.bus_route,
                                              start_time__gte=time_now)

        for brj in brjs:
            create_single_bus_route_town_stoppage_journey(
                brj, bus_route_town_stoppage)

        return None

    @classmethod
    def delete_bus_route_town_stoppage(cls, bus_route_town_stoppage):
        BusRouteTownStoppageJourney.objects.filter(
            bus_route_town_stoppage=bus_route_town_stoppage).delete()
        bus_route_town_stoppage.delete()


def sync_bus_route_town_stoppage_time():
    bus_route_town_stoppages = BusRouteTownStoppage.objects.all()

    for bus_route_town_stoppage in bus_route_town_stoppages:
        bus_route_town = bus_route_town_stoppage.bus_route_town
        bus_route = bus_route_town.bus_route
        bus_route_start_time = bus_route.start_time
        total_duration = bus_route_town.duration + bus_route_town_stoppage.duration
        bus_route_town_stoppage_start_time = get_time_from_duration(
            bus_route_start_time, total_duration)
        bus_route_town_stoppage.start_time = bus_route_town_stoppage_start_time
        bus_route_town_stoppage.save()
