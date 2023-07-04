from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models.operators import Operator

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

    # def create(self, request):
    #     mobile_number = request.data.get('mobile')

    #     # Retrieve the user based on the mobile number
    #     try:
    #         operator = Operator.objects.get(mobile=mobile_number)
    #     except:
    #         return Response({'error': 'Invalid Mobile Number'}, status=400)

    #     # Create a new bus object
    #     request.data['operator'] = operator.id

    #     serializer = BusSerializer(data=request.data)
    #     if serializer.is_valid():
    #         bus = serializer.save()
    #         data = self.get_serializer(bus).data
    #         return Response({'success': 'Bus created successfully', 'data': data}, status=201)
    #     else:
    #         return Response(serializer.errors, status=400)

    # def retrieve(self, request, *args, **kwargs):
    #     mobile = self.request.data.get('mobile')

    #     # print("###################", mobile)
    #     # Retrieve the user based on the mobile number
    #     try:
    #         operator = Operator.objects.filter(
    #             mobile=mobile).values_list('id', flat=True).first()
    #         # print('###############', operator)
    #     except:
    #         return Response({'error': 'Invalid Mobile Number'}, status=400)

    #     bus = Bus.objects.filter(operator=operator)
    #     serializer = self.get_serializer(bus, many=True)
    #     data = serializer.data
    #     return Response({'success': 'Bus fetched successfully', 'data': data}, status=200)

    # def update(self, request, *args, **kwargs):
    #     # lookup_field = 'bus_number'

    #     bus_number = self.request.data.get('bus_number')
    #     # # partial = kwargs.pop('partial', False)
    #     # instance = self.get_object()
    #     # print('###############', instance)
    #     # serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     # serializer.is_valid(raise_exception=True)
    #     # self.perform_update(serializer)
    #     # return Response(serializer.data)

    #     try:
    #         instance = Bus.objects.filter(
    #             bus_number=bus_number).values()#.values_list('id', flat=True).first()
    #         # print('###############', operator)
    #     except:
    #         return Response({'error': 'Invalid Bus Number'}, status=400)

    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=True)
    #     print('#################',serializer)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response({'success': 'Bus updated successfully', 'data': serializer.data}, status=200)
