import uuid
from rest_framework import generics, status
from pricing.models.price import PriceMatrix
# from bus.models.bus_route import BusRoute
# from bus.models.bus_route_journey import BusRouteJourney
from pricing.serializers.price import PriceSerializer
# from account.models.operators import Operator
from utils.restful_response import send_response
from utils.apnibus_logger import apnibus_logger
# from bus.pagination import AdminBusListPagination, BusListPagination
# from utils.exception_handler import get_object_or_json404
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from bus.helpers.ticket_header import update_ticket_header
# from operators.helpers.remarks import add_remarks


class CreatePriceView(generics.CreateAPIView):
    """
    working: Used for adding a bus.
    """

    serializer_class = PriceSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """
        :param request: operator_id and required fields to create a bus in DB.
        :return: Created bus JSON object.
        """
        # operator_id = request.data.get('operator_id', None)
        # operator_instance = Operator.objects.filter(id=operator_id).first()

        serializer = self.get_serializer(data=request.data)
        # price_matrix = request.data.get('price_matrix', None)
        # print("1", request.data)
        # print("2", serializer.is_valid())
        if serializer.is_valid():
            instance = serializer.save()

            # remarks = request.data.get('remarks', None)

            # if remarks:
            #     add_remarks(remarks, request.user.id, "BUS", bus_id=instance.id)

            # Update bus ticket header text
            # update_ticket_header(instance)

            data = self.get_serializer(instance).data
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                             ui_message='Invalid data', error=serializer.errors)


class PriceListView(generics.ListAPIView):
    """
    working: Used to get list of buses in DB.
    """

    serializer_class = PriceSerializer
    queryset = PriceMatrix.objects.all()
    # pagination_class = AdminBusListPagination

    def list(self, request, *args, **kwargs):
        """
        :param request: bus_id - Pass bus_id in params if you want to see info of a particular bus.
        :param request: company_name - Pass company_name in params if you want to see buses of a particular company.
        :param request: operator_mobile_number - Pass operator_mobile_number in params if you want to see buses of a particular operator.
        :return: JSON objects of desired buses.
        """

        queryset = PriceMatrix.objects.all()
        bus_route = request.GET.get('bus_route', None)
        print("#########", bus_route)
        # company_name = request.GET.get('company_name', None)
        # operator_mobile_number = request.GET.get(
        # 'operator_mobile_number', None)
        if bus_route:
            queryset = queryset.filter(bus_route_id=bus_route)
            print(queryset)

        # if company_name:
        #     queryset = queryset.filter(operator__name__icontains=company_name)

        # if operator_mobile_number:
        #     queryset = queryset.filter(operator__mobile__contains=operator_mobile_number)

        # page = self.paginate_queryset(queryset)
        # serializer = self.get_serializer(page, many=True)
        # response = self.get_serializer(request.data)
        # response = self.get_paginated_response(serializer.data)
        # return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
        #                      data=response.data)
        fields = ('id', 'bus_route', 'price_matrix')
        data = self.get_serializer(queryset, many=True, fields=fields).data
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)


class PricingUpdateView(generics.UpdateAPIView):
    queryset = PriceMatrix.objects.all()
    serializer_class = PriceSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'bus_route'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        apnibus_logger.info(request.data)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            # with transaction.atomic():
            #     operator_email = request.data.get('email', None)

            # if operator_email:
            #     operator_serializer = serializer.save()
            #     operator_serializer.user.email = operator_email
            #     operator_serializer.user.save()
            #     operator_serializer.save()

            price_bus_route = request.data.get('bus_route', None)
            if price_bus_route:
                price_serializer = serializer.save()
            pricing_matrix = request.data.get('price_matrix', None)
            if pricing_matrix:
                price_serializer = serializer.save()
            # if operator_status:
            #     operator_serializer = serializer.save()
            #     if operator_status == Operator.DEBOARDED:
            #         operator_serializer.subscription_pending = True
            #         operator_serializer.save()
            #     if operator_status == Operator.ONBOARDED:
            #         operator_serializer.subscription_pending = False
            #         operator_serializer.save()
            #     if operator_status == Operator.LOCKED:
            #         operator_serializer.subscription_pending = True
            #         operator_serializer.save()

            price_serializer = serializer.save()

            # remarks = request.data.get('remarks', None)
            # if remarks:
            #     add_remarks(remarks, request.user.id, "OPERATOR", operator_id=operator_serializer.id)
            #
            # if request.data.get('bank_accounts', None):
            #     operator_account_obj = OperatorBankAccount.objects.filter(operator=instance).first()
            #     operator_account_serializer = OperatorBankAccountSerializer(
            #         operator_account_obj,
            #         data=request.data.get('bank_accounts')[0],
            #         partial=True
            #     )
            #     if operator_account_serializer.is_valid():
            #         operator_account_serializer.save(operator=operator_serializer)
            data = self.get_serializer(price_serializer).data
            return send_response(status.HTTP_200_OK, data=data, developer_message='Request was successful.')

        return send_response(status=status.HTTP_400_BAD_REQUEST, error=serializer.errors,
                             developer_message='Request failed due to invalid data.')


class DeletePricingView(generics.DestroyAPIView):
    """
    working: Used to delete a particular bus using bus number.
    """

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        print("############", request)
        # bus_route_id = request.GET.get('bus_route')
        bus_route_id = uuid.UUID(request.path.split('/')[-1]) 
        # print("############", request.path.split('/')[-1])
        price_obj = PriceMatrix.objects.filter(
            bus_route_id=bus_route_id).first()
        print("############", price_obj)
        # bus_routes = BusRoute.objects.filter(bus=bus_obj)
        # bus_routes.delete()
        price_obj.delete()

        return send_response(
            status=status.HTTP_200_OK,
            developer_message="Request was successful.",
            ui_message="Request was successful"
        )

# class BusRetrieveView(generics.RetrieveAPIView):
#     """
#     working: Used to retrieve info of a particular bus using bus id.
#     """

#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#     lookup_field = 'id'

#     def retrieve(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#         except Exception as e:
#             return send_response(status.HTTP_400_BAD_REQUEST,
#                                  developer_message='Request has failed because of invalid bus_number',
#                                  ui_message='The bus_number you\'re tyring to access does not exist')
#         serializer = self.get_serializer(instance)
#         return send_response(status.HTTP_200_OK, data=serializer.data,
#                              developer_message='Request was success')


# class BusUpdateView(generics.UpdateAPIView):
#     """
#     working: Used to update info of bus that already exists.
#     """

#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#     lookup_field = 'id'

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         operator_id = request.data.get('operator_id', None)

#         serializer = self.get_serializer(
#             instance, data=request.data, partial=True)

#         if serializer.is_valid():
#             if operator_id:
#                 operator = get_object_or_json404(
#                     Operator.objects.all(), id=operator_id)
#                 instance = serializer.save(operator=operator)
#             instance = serializer.save()

#             # remarks = request.data.get('remarks', None)

#             # if remarks:
#             #     add_remarks(remarks, request.user.id, "BUS", bus_id=instance.id)

#             data = self.get_serializer(instance).data
#             return send_response(status.HTTP_200_OK, data=data, developer_message='Request was successful.')

#         return send_response(status=status.HTTP_400_BAD_REQUEST, error=serializer.errors,
#                              developer_message='Request failed due to invalid data.')


# class BusSearchView(generics.ListAPIView):
#     """
#     working: Used to search buses using their number.
#     :return: List of targeted buses.
#     """
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.queryset
#         bus_number = request.GET.get('bus_number')
#         queryset = queryset.filter(number__icontains=bus_number)

#         fields = ('id', 'number', 'category')
#         data = self.get_serializer(queryset, many=True, fields=fields).data
#         return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
#                              data=data)


# class DeleteBusView(generics.DestroyAPIView):
#     """
#     working: Used to delete a particular bus using bus number.
#     """

#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def delete(self, request, *args, **kwargs):
#         bus_number = request.GET.get('bus_number')
#         bus_obj = Bus.objects.filter(number=bus_number).first()
#         bus_routes = BusRoute.objects.filter(bus=bus_obj)
#         bus_routes.delete()
#         bus_obj.delete()

#         return send_response(
#             status=status.HTTP_200_OK,
#             developer_message="Request was successful.",
#             ui_message="Request was successful"
#         )
