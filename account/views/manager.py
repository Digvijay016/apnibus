# import uuid
# from rest_framework import generics, status
# from account.serializers import ManagerSerializer
# from account.models import Operator
# from account.models import User
# from utils.restful_response import send_response
# from account.models.manager import Manager

# from bus.models import Bus


# class ManagerView(generics.ListCreateAPIView):
#     queryset = Manager.objects.all()
#     serializer_class = ManagerSerializer

#     def get_queryset(self):
#         queryset = Manager.objects.all()
#         operator_id = self.request.GET.get('operator_id', None)
#         mobile = self.request.GET.get('mobile', None)

#         if operator_id:
#             queryset = queryset.filter(operator_id=operator_id)

#         if mobile:
#             queryset = queryset.filter(mobile=mobile)

#         return queryset

#     def create(self, request, *args, **kwargs):
#         operator_id = request.data.get('operator_id', None)

#         if not operator_id:
#             pass

#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             operator = Operator.objects.get(id=operator_id)
#             user = User.objects.create(username=uuid.uuid1(), user_type=User.MANAGER)
#             serializer.save(operator=operator, user=user)

#             return send_response(status=status.HTTP_201_CREATED, data=serializer.data,
#                                  developer_message="Request was successful.",
#                                  ui_message="Request was successful.",
#                                  )
#         return send_response(status=status.HTTP_201_CREATED, error=serializer.errors,
#                              developer_message="Request failed",
#                              ui_message="Request failed",
#                              )


# class ManagerMapToBusView(generics.CreateAPIView):
#     def create(self, request, *args, **kwargs):
#         bus_id = request.data.get('bus_id', None)
#         manager_id = request.data.get('manager_id', None)

#         if not bus_id or not manager_id:
#             return send_response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 developer_message="Please add both bus_id and manager_id",
#                 ui_message="Please add both bus_id and manager_id",
#             )

#         bus_obj = Bus.objects.get(id=bus_id)
#         manager_obj = Manager.objects.get(id=manager_id)

#         if str(bus_obj.operator.id) != str(manager_obj.operator.id):
#             return send_response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 developer_message="Operator not matching",
#                 ui_message="Operator not matching",
#             )

#         bus_obj.managers.add(manager_obj)

#         return send_response(
#             status=status.HTTP_200_OK,
#             developer_message="Request Success",
#             ui_message="Request Success",
#         )


# class ManagerRemoveMapToBusView(generics.UpdateAPIView):
#     def update(self, request, *args, **kwargs):
#         bus_id = request.data.get('bus_id', None)
#         manager_id = request.data.get('manager_id', None)

#         if not bus_id or not manager_id:
#             return send_response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 developer_message="Please add both bus_id and manager_id",
#                 ui_message="Please add both bus_id and manager_id",
#             )

#         bus_obj = Bus.objects.get(id=bus_id)
#         manager_obj = Manager.objects.get(id=manager_id)

#         if str(bus_obj.operator.id) != str(manager_obj.operator.id):
#             return send_response(
#                 status=status.HTTP_400_BAD_REQUEST,
#                 developer_message="Operator not matching",
#                 ui_message="Operator not matching",
#             )

#         bus_obj.managers.remove(manager_obj)

#         return send_response(
#             status=status.HTTP_200_OK,
#             developer_message="Request Success",
#             ui_message="Request Success",
#         )

