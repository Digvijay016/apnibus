from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models.operators import Operator
from utils.restful_response import send_response
import json
from bus.models.bus import Bus
from bus.serializers.bus import BusSerializer


class CreateBusView(viewsets.ModelViewSet):
    """
    working: Used for adding a bus.
    """

    # serializer_class = BusSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'operator'

    def create(self, request, *args, **kwargs):
        bus_number = request.data.get('bus_number',None)
        pos_serial_img = request.data.get('pos_serial_no',None)
        gps_sim_img = request.data.get('gps_sim_image',None)

        error = ''

        if not bus_number:
            error = 'Please enter bus number.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not pos_serial_img:
            error = 'Please select pos serial image.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not gps_sim_img:
            error = 'Please select gps sim image.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        serializer = self.get_serializer(data=request.data)
        print(request.META)
        # data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

            return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Bus created successfully.',
                                     data=data)
        # error = 'Serialization Failed'
        return send_response(status=status.HTTP_200_OK, error_msg=json.dumps(serializer.errors) ,developer_message='Request Failed.',
                                     data='')

    def get_queryset(self):
        operator_id = self.request.query_params.get('operator')
        if operator_id:
            print("#######################",operator_id)
            query_set = Bus.objects.filter(operator=operator_id)
            print("#######################",query_set)
            return query_set
        else:
            return self.queryset
