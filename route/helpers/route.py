from route.models import Route, RouteTown, RouteTownStoppage, RouteTownStoppage
from route.models import Town


def clone_route(route_id, new_route_name, via, new_towns, duration_from_first_town, distance_from_first_town):
    main_route_obj = Route.objects.get(id=route_id)

    new_route_obj = Route.objects.create(
        from_town=main_route_obj.from_town, to_town=main_route_obj.to_town,
        name=f"Copy of - {main_route_obj.name}", via=main_route_obj.via,
        is_default=main_route_obj.is_default, status=main_route_obj.status,
    )

    new_route_obj.via = via

    if new_route_name:
        new_route_obj.name = new_route_name

    new_route_obj.save()

    # Creating Route Towns and route Town Stoppages
    main_route_towns = RouteTown.objects.filter(route=main_route_obj)
    main_route_stoppages = RouteTownStoppage.objects.filter(
        route_town__route=main_route_obj)

    for main_route_town in main_route_towns:

        new_route_town = RouteTown.objects.create(
            route=new_route_obj, town=main_route_town.town,
            duration=main_route_town.duration + duration_from_first_town,
            distance=main_route_town.distance + distance_from_first_town,
            status=main_route_town.status
        )

        main_route_town_stoppages = main_route_stoppages.filter(
            route_town=main_route_town)

        for main_route_town_stoppage in main_route_town_stoppages:
            RouteTownStoppage.objects.create(
                route_town=new_route_town, town_stoppage=main_route_town_stoppage.town_stoppage,
                duration=main_route_town_stoppage.duration, status=main_route_town_stoppage.status
            )

    for new_town in new_towns:
        town_id = new_town['town_id']
        duration = new_town['duration']
        distance = new_town['distance']

        RouteTown.objects.create(
            route=new_route_obj, town=Town.objects.get(id=town_id),
            duration=duration, distance=distance)

    return new_route_obj


def reverse_route(route_id):
    route_created = False
    new_route = None
    route = Route.objects.get(id=route_id)

    if not route.reverse_route_exists:
        try:
            new_route_name = f"{route.to_town.name}-{route.from_town.name} via {route.via}"
            new_route = Route.objects.create(
                from_town=route.to_town,
                to_town=route.from_town,
                via=route.via,
                status=route.status,
                name=new_route_name,
                reverse_route_exists=True
            )
            route_towns = RouteTown.objects.filter(
                route=route).order_by('-duration')
            if route_towns:
                last_route_town_duration = route_towns[0].duration
                last_route_town_distance = route_towns[0].distance

                i = 1
                for route_town in route_towns:
                    route_town_stoppages = RouteTownStoppage.objects.filter(
                        route_town=route_town).order_by('-duration')
                    new_town_duration = last_route_town_duration - route_town.duration
                    new_town_distance = last_route_town_distance - route_town.distance

                    new_route_town = RouteTown.objects.create(
                        route=new_route,
                        town=route_town.town,
                        duration=new_town_duration,
                        distance=new_town_distance,
                        status=route_town.status
                    )

                    i += 1

                    if route_town_stoppages:
                        last_route_town_stoppage_duration = route_town_stoppages[0].duration

                        for route_town_stoppage in route_town_stoppages:
                            new_town_stoppage_duration = last_route_town_stoppage_duration - \
                                route_town_stoppage.duration

                            RouteTownStoppage.objects.create(
                                route_town=new_route_town,
                                town_stoppage=route_town_stoppage.town_stoppage,
                                duration=new_town_stoppage_duration,
                                status=route_town_stoppage.status
                            )

            route_created = True
            route.reverse_route_exists = True
            route.save()
        except Exception as ex:
            print(ex)

    return route_created, new_route
