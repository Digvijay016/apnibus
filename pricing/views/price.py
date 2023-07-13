from rest_framework import viewsets
from pricing.models.price import PriceMatrix
from pricing.serializers.price import PriceSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreatePriceView(viewsets.ModelViewSet):
    """
    working: Used for adding a bus.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = PriceMatrix.objects.all()
    serializer_class = PriceSerializer

    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request):
        # Saving Pricing
        json_body = json.loads(request.body);

        error= ''

        if not json_body:
            error = 'Please enter request body in json format.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                    developer_message='Request failed due to invalid data.')
        
        serializer = self.get_serializer(data=json_body)
        data = ''
        if serializer.is_valid():
            instance = serializer.save()
            data = self.get_serializer(instance).data

        # Return a success response
            return send_response(status=status.HTTP_200_OK, error_msg='' ,developer_message='Pricing for Bus Route created successfully.',
                                     data=data)
        return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors ,developer_message='Request failed due to invalid data.',
                                     data='')
