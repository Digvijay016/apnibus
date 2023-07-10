import json
from rest_framework import viewsets, status
from bus.models.bus_routes_towns import BusRoutesTowns
from bus.serializers.bus_routes_towns import BusRoutesTownsSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response


class CreateBusRoutesTownsView(viewsets.ModelViewSet):
    """
    working: Used to create bus route town.
    """

    queryset = BusRoutesTowns.objects.all()
    serializer_class = BusRoutesTownsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    http_method_names = ['get', 'post', 'put', 'delete']
    # lookup_field = 'route'

    def create(self, request):
        json_body = json.loads(request.body);

        error= ''

        if not json_body:
            error = 'Please enter request body in json format.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')
            
        json_body['towns'] = sorted(json_body['towns'], key=lambda x:x['duration'])

        print("###############################################################")
        print(json_body['towns'])
        print("###############################################################")

        serializer = self.get_serializer(data=json_body)
        data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

        # Return a success response
        # return JsonResponse({'message': 'Bus route towns created successfully', 'data': data}, status=201)
        return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Bus Route Town created successfully.',
                                     data=data)

    def get_queryset(self):
        route_id = self.request.query_params.get('route')
        if route_id:
            print("#######################",route_id)
            query_set = BusRoutesTowns.objects.filter(route=route_id)
            print("#######################",query_set)
            return query_set
        else:
            return self.queryset
