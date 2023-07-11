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

        error= ''

        if not json_body:
            error = 'Please enter request body in json format.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        missing_towns_qs = BusRouteMissingTown.objects.all()
        missing_towns_uid = [
            str(uid) for uid in missing_towns_qs.values_list('id',flat=True)
        ]

        print("########################## 1",str(json_body['bus_route']))

        for uid in missing_towns_uid:
            bus_route = BusRouteMissingTown.objects.filter(id=uid).values_list('bus_route',flat=True).first()
            missing_town_name = BusRouteMissingTown.objects.filter(id=uid).values_list('missing_town',flat=True).first()
            duration = BusRouteMissingTown.objects.filter(id=uid).values_list('duration',flat=True).first()

            print("########################## 2",str(bus_route))

            if str(bus_route) == str(json_body['bus_route']):
                missing_town_dct = {
                    'missing_town_id':uid,
                    'missing_town_name':missing_town_name,
                    'duration':duration,
                    'missing_town_status':'inactive',
                    'stoppage':[]
                }
                json_body['towns'].append(missing_town_dct)
            
        json_body['towns'] = sorted(json_body['towns'], key=lambda x:x['duration'])

        print("############################################################### 3")
        print(json_body['towns'])
        print("###############################################################")

        serializer = self.get_serializer(data=json_body)
        data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

        # Return a success response
        # return JsonResponse({'message': 'Bus route towns created successfully', 'data': data}, status=201)
            return send_response(status=status.HTTP_200_OK, error_msg='' ,developer_message='Bus Route Town created successfully.',
                                     data=data)
        return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors ,developer_message='Request failed due to invalid data.',
                                     data='')
