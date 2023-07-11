from rest_framework import viewsets, status
from account.models.operators import Operator
from utils.restful_response import send_response
from account.serializers.operator import OperatorSerializer
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

    filter_backends = [SearchFilter]
    search_fields = ['status']

    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
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
            user = SalesTeamUser.objects.filter(username = self.request.user).values_list('username',flat=True).first()
            serializer.validated_data['username'] = str(user)
            instance = serializer.save()
            data = self.get_serializer(instance).data

            return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Operator created successfully.',
                                     data=data)

        return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors ,developer_message='Serialization Error.',
                                     data='')
        

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.query_params.get('status', None)

        if search_param:
            queryset = queryset.filter(status__icontains=search_param, username = self.request.user)

        return queryset

# from functools import partial
# import uuid
# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import action
# from account.helpers.otp import send_otp
# from account.helpers.otp_service import OTPService
# from account.serializers.commuter import UserOTPGenerationSerializer
# from account.models.operators import Operator
# from utils.restful_response import send_response
# from account.models.user_authentication import UserAuthenticationOTP
# from account.models.user import User
# from account.serializers.operator import OperatorSerializer
# from utils.apnibus_logger import apnibus_logger
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from utils.sms_service import MSG91_TEMPLATE_IDS, MSG91Service
# from django.db.models import Q, Sum
# from django_filters.rest_framework import DjangoFilterBackend
# # from django.db.models import Value


# class OperatorUserAuthOTPViewset(viewsets.ModelViewSet):
#     """
#     A viewset that provides the API related to Operator on-boarding/login
#     """
#     queryset = UserAuthenticationOTP.objects.all()
#     serializer_class = UserOTPGenerationSerializer
#     error = ''

#     def create(self, request, *args, **kwargs):
#         mobile = request.data.get('mobile')
#         if not mobile.isnumeric() or len(mobile) != 10:
#             error = 'Invalid mobile number.Mobile number must be of 10 digits.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')
#         operator_obj = Operator.objects.filter(mobile=mobile).first()
#         if not operator_obj:
#             return send_response(status=status.HTTP_400_BAD_REQUEST, error_msg='User doesn\'t exist.', developer_message='Request failed due to invalid data.')

#         else:
#             # Invalidate previous OTPs
#             UserOTPGenerationSerializer.invalidate_otp(mobile)

#         serializer = UserOTPGenerationSerializer(data=request.data)

#         if serializer.is_valid():
#             new_otp_created, otp = OTPService().resend_otp(mobile)
#             user_obj = operator_obj.user

#             # Sending otp through msg91
#             template_id = MSG91_TEMPLATE_IDS['SEND_OTP']
#             variable_list = [otp, ""]
#             msg_sent = MSG91Service(
#                 mobile, template_id, variable_list).send_sms()

#             if not msg_sent:
#                 send_otp(user_obj, mobile, otp)
#                 print("Msg sent using TextLocal Service")
#             else:
#                 print("Msg sent using MSG91 Service")

#             apnibus_logger.info(otp, mobile)
#             if new_otp_created:
#                 serializer.save(user=user_obj, otp=otp)
#             return send_response(status=status.HTTP_200_OK,error_msg='', developer_message='Request was successful')

#         else:
#             return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors,
#                                  developer_message='Request failed due to invalid data.')

#     @action(methods=['put'], detail=True)
#     def verify(self, request, *args, **kwargs):
#         mobile = request.data.get('mobile')
#         if not mobile.isnumeric() or len(mobile) != 10:
#             error = 'Invalid mobile number.Mobile number must be of 10 digits.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')
#         otp = request.data.get('otp')
#         apnibus_logger.info(mobile, otp)
#         valid_otp = UserAuthenticationOTP.objects.filter(mobile=mobile, otp=otp, is_valid=True,
#                                                          is_verified=False).first()

#         if valid_otp:
#             operator_obj = Operator.objects.filter(contact=mobile).first()
#             user = operator_obj.user
#             if not user:
#                 user = User.objects.create(
#                     username=uuid.uuid1(), user_type=User.OPERATOR)
#                 operator_obj.user = user
#                 operator_obj.save()
#             token_obj, is_created = Token.objects.get_or_create(user=user)
#             auth_token = token_obj.key

#             data = {}
#             data['auth_token'] = auth_token
#             user.is_active = True
#             user.save()
#             valid_otp.is_valid = False
#             valid_otp.is_verified = True
#             valid_otp.save()

#             return send_response(status=status.HTTP_200_OK, error_msg='',
#                                  developer_message='Request was successful.', data=data)
#         return send_response(status=status.HTTP_401_UNAUTHORIZED, error_msg='Wrong otp',
#                              developer_message='Invalid otp or mobile number')


# class CreateOperatorView(viewsets.ModelViewSet):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     queryset = Operator.objects.all()
#     serializer_class = OperatorSerializer

#     filter_backends = [
#             #SearchFilter, 
#             OrderingFilter, 
#             DjangoFilterBackend
#             ]
#     ordering_fields = ['created_on', 'updated_on']
#     ordering = ['created_on']
#     #search_fields = ['status']
#     filterset_fields = ['status']

#     http_method_names = ['get', 'post', 'put', 'delete']

#     def create(self, request, *args, **kwargs):
#         mobile = request.data.get('mobile',None)
#         adhar_front_img = request.data.get('aadhar_front_photo', None)
#         adhar_back_img = request.data.get('aadhar_back_photo', None)
#         pan_img = request.data.get('pan_photo', None)
#         user = self.request.user
#         error=''

#         if mobile is None:
#             serializer = self.get_serializer(data=request.data)
#             data = ''
#             if serializer.is_valid():
#                 instance = serializer.save()
#                 data = self.get_serializer(instance).data

#             return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Operator created successfully.',
#                                         data=data)

#         if not mobile.isnumeric() or len(mobile) != 10:
#             error = 'Invalid mobile number.Mobile number must be of 10 digits.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')
#             if mobile:
#                 operator_mobile = Operator.objects.filter(mobile=mobile).values_list('mobile',flat=True).first()
#                 if operator_mobile:
#                     return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed.User already exists.Please use different mobile.')

#         if not adhar_front_img:
#             error = 'Please select adhar front photo.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')

#         if not adhar_back_img:
#             error = 'Please select adhar back photo.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')

#         if not pan_img:
#             error = 'Please select pan photo.'
#             return send_response(status=status.HTTP_200_OK, error_msg=error,
#                                  developer_message='Request failed due to invalid data.')

#         serializer = self.get_serializer(data=request.data)
#         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",serializer)
#         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",serializer.is_valid())
#         # data = ''
#         headers = request.META
#         print("####################### Headers Operator",headers)
#         if serializer.is_valid():
#             instance = serializer.save()
#             data = self.get_serializer(instance).data
#             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@",data)
#             return send_response(status=status.HTTP_200_OK, error_msg=error ,developer_message='Operator created successfully.',
#                                      data=data)
#         return send_response(status=status.HTTP_200_OK, error_msg=serializer.errors ,developer_message='Request failed.',
#                                      data="")

#         # Return a success response
#         # return JsonResponse({'message': 'Operator created successfully', 'data': data}, status=201)

        

#     """def get_queryset(self):
#         queryset = super().get_queryset()
#         search_param = self.request.query_params.get('status', None)
#         user = self.request.user

#         print("################################## user",user)

#         if search_param:
#             queryset = queryset.filter(status__icontains=search_param,user=user)

#         # queryset = queryset.filter(user=user)

#         return queryset"""

#     # lookup_field = 'mobile'

#     # def get_queryset(self):
#     #     queryset = super().get_queryset()
#     #     mobile_number = self.request.data.get('mobile', None)
#     #     if mobile_number:
#     #         queryset = queryset.filter(mobile=mobile_number)
#     #     return queryset

#     # def update(self, request, *args, **kwargs):
#     #     mobile_number = self.request.data.get('mobile', None)
#     #     instance = self.get_object()
#     #     if mobile_number and instance.mobile == mobile_number:
#     #         serializer = self.get_serializer(
#     #             instance, data=request.data, partial=True)
#     #         serializer.is_valid(raise_exception=True)
#     #         serializer.perform_update(serializer)
#     #         return Response(serializer.data)
#     #     else:
#     #         return Response({'detail': 'Invalid mobile number'}, status=status.HTTP_400_BAD_REQUEST)
