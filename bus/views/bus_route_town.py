from rest_framework import viewsets, status
from bus.models.bus import Bus
from django.http import JsonResponse
from bus.models.bus_route import BusRoute
from bus.models.bus_route_town import BusRouteTown
from bus.models.bus_routes_towns import BusRoutesTowns
from bus.models.bus_route_missing_town import BusRouteMissingTown
from bus.serializers.bus_route_town import BusRouteTownSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response

import json
# from utils.exception_handler import get_object_or_json404


class CreateBusRouteTownView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRouteTown.objects.all()
    serializer_class = BusRouteTownSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']

    # def get_queryset(self):
    #     bus_id = self.request.query_params.get('bus')
    #     if bus_id:
    #         print("#######################", bus_id)
    #         queryset_bus_route = BusRoute.objects.filter(bus=bus_id)
    #         print("#######################", queryset_bus_route)
    #         if queryset_bus_route:
    #             for qs in queryset_bus_route:
    #                 print("#############################",qs)
    #                 queryset_bus_route_town = BusRouteTown.objects.filter(bus_route=qs)
    #                 print("#######################", queryset_bus_route_town)
    #         return queryset_bus_route_town
    #     else:
    #         return self.queryset

    def create(self, request):
        # Extract the 'towns' data from the parsed JSON

        json_body = json.loads(request.body);
        print("###############################################################")
        print(json_body)
        print("###############################################################")

        error= ''

        if not json_body:
            error = 'Please enter request body in json format.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        # route = request.data.get('route')
        # town_id = request.data.get('town_id')
        # town_stoppage_id = request.data.get('town_stoppage_id')
        # town_status = request.data.get('town_status')
        # town_stoppage_status = request.data.get('town_stoppage_status')

        # print("##########################", route)
        # print("##########################", town_id)
        # print("##########################", town_stoppage_id)
        # print("##########################", town_status)
        # print("##########################", town_stoppage_status)

        # queryset = BusRoutesTowns.objects.all()
        # towns = queryset.values_list('towns', flat=True)
        # towns = list(towns)
        # towns = towns[0]
        # print("##########################", towns)

        # for town in towns:
        #     townId = town.get('town_id')
        #     townStoppageId = town.get('town_stoppage_id')
        #     if town_id == townId:
        #         town['town_status'] = town_status

        #     if town_stoppage_id == townStoppageId:
        #         town['town_stoppage_status'] = town_stoppage_status

        # # missing_towns_qs = BusRouteMissingTown.objects.all()
        

        serializer = self.get_serializer(data=json_body)
        data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

        # Return a success response
        # return JsonResponse({'message': 'Bus route towns created successfully', 'data': data}, status=201)
        return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Bus Route Town created successfully.',
                                     data=data)
