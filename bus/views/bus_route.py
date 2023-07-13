from http.client import responses
from rest_framework import viewsets, status
from bus.models.bus_route import BusRoute
from bus.serializers.bus_route import BusRouteSerializer
from bus.models.bus_route import BusRoute
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response


class CreateBusRouteView(viewsets.ModelViewSet):
    """
    working: Used to create bus route.
    """

    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        bus = request.data.get('bus',None)
        from_town = request.data.get('from_town',None)
        to_town = request.data.get('to_town',None)
        start_time = request.data.get('start_time',None)
        arrival_time = request.data.get('arrival_time',None)
        return_id = request.data.get('return_id',None)

        error = ''

        if not bus and not return_id:
            error = 'Please enter bus Id.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not from_town and not return_id:
            error = 'Please enter from_town Id.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not to_town and not return_id:
            error = 'Please enter to_town Id.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not start_time:
            error = 'Please enter start_time.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not arrival_time:
            error = 'Please enter arrival_time.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')


        serializer = self.get_serializer(data=request.data)
        data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

        return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Bus Route created successfully.',
                                     data=data)


    def get_queryset(self):
        bus_id = self.request.query_params.get('bus')
        if bus_id:
            query_set = BusRoute.objects.filter(bus=bus_id)
            return query_set
        else:
            return self.queryset
