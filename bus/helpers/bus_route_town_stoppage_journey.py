from datetime import timedelta
from bus.models.bus_route_town_stoppage import BusRouteTownStoppage
from bus.models.bus_route_town_stoppage_journey import BusRouteTownStoppageJourney


def create_bus_route_town_stoppage_journeys(bus_route_journey):
    brts = BusRouteTownStoppage.objects.filter(
        bus_route_town__bus_route=bus_route_journey.bus_route)
    for item in brts:
        create_single_bus_route_town_stoppage_journey(bus_route_journey, item)


def create_single_bus_route_town_stoppage_journey(bus_route_journey, bus_route_town_stoppage):
    instance, is_created = BusRouteTownStoppageJourney.objects.get_or_create(
        bus_route_journey=bus_route_journey,
        bus_route_town_stoppage=bus_route_town_stoppage,
    )

    # update below values only when new obj is created
    if is_created:
        instance.latitude = bus_route_town_stoppage.latitude
        instance.longitude = bus_route_town_stoppage.longitude
        total_duration = bus_route_town_stoppage.bus_route_town.duration + \
            bus_route_town_stoppage.duration

        instance.arrival_time = bus_route_journey.start_time + \
            timedelta(minutes=total_duration)
        instance.save()

    return instance
