from rest_framework import viewsets, status
from account.models.operators import Operator
from utils.restful_response import send_response
from account.serializers.operator import OperatorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from account.models.sales_team import SalesTeamUser
from utils.apnibus_logger import apnibus_logger
from rest_framework.filters import SearchFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateOperatorView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, **kwargs):

        mobile = request.data.get('mobile',None)
        adhar_front_img = request.data.get('aadhar_front_photo', None)
        adhar_back_img = request.data.get('aadhar_back_photo', None)
        pan_img = request.data.get('pan_photo', None)
        error=''

        if mobile is None:
            serializer = self.get_serializer(data=request.data)
            data = ''
            if serializer.is_valid():
                instance = serializer.save()
                data = self.get_serializer(instance).data

            return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Operator created successfully.',
                                        data=data)

        if not mobile.isnumeric() or len(mobile) != 10:
            error = 'Invalid mobile number.Mobile number must be of 10 digits.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not adhar_front_img:
            error = 'Please select adhar front photo.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not adhar_back_img:
            error = 'Please select adhar back photo.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not pan_img:
            error = 'Please select pan photo.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        serializer = self.get_serializer(data=request.data)
        data = ''

        if serializer.is_valid():
            print(self.request.user.id)
            serializer.validated_data['sales_user_id'] = self.request.user.id
            instance = serializer.save()
            data = self.get_serializer(instance).data

            return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Operator created successfully.',
                                     data=data)

        return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors ,developer_message='Serialization Error.',
                                     data='')
        

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(sales_user_id = self.request.user.id)
        return queryset
