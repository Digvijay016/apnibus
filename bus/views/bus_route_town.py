import json
from urllib import request
from rest_framework import viewsets  # , generics, status
from bus.models.bus import Bus
from django.http import JsonResponse
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_routes_towns import BusRoutesTowns
from bus.serializers.bus_route_town import BusRouteTownSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.exception_handler import get_object_or_json404


class CreateBusRouteTownView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRouteTown.objects.all()
    serializer_class = BusRouteTownSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']


    def create(self, request):
        # Extract the 'towns' data from the parsed JSON
        route = request.data.get('route')
        town_id = request.data.get('town_id')
        town_stoppage_id = request.data.get('town_stoppage_id')
        town_status = request.data.get('town_status')
        town_stoppage_status = request.data.get('town_stoppage_status')

        print("##########################", route)
        print("##########################", town_id)
        print("##########################", town_stoppage_id)
        print("##########################", town_status)
        print("##########################", town_stoppage_status)

        queryset = BusRoutesTowns.objects.all()
        towns = queryset.values_list('towns', flat=True)
        towns = list(towns)
        towns = towns[0]
        print("##########################", towns)

        for town in towns:
            townId = town.get('town_id')
            townStoppageId = town.get('town_stoppage_id')
            if town_id == townId:
                town['town_status'] = town_status

            if town_stoppage_id == townStoppageId:
                town['town_stoppage_status'] = town_stoppage_status

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(towns=towns)
            data = self.get_serializer(instance).data

        # Return a success response
        return JsonResponse({'message': 'Bus route towns created successfully', 'data': data}, status=201)
