from functools import partial
import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from account.helpers.otp import send_otp
from account.helpers.otp_service import OTPService
from account.serializers.commuter import UserOTPGenerationSerializer
from account.models.operators import Operator
from utils.restful_response import send_response
from account.models.user_authentication import UserAuthenticationOTP
from account.models.user import User
from account.serializers.operator import OperatorSerializer
from utils.apnibus_logger import apnibus_logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.sms_service import MSG91_TEMPLATE_IDS, MSG91Service


class OperatorUserAuthOTPViewset(viewsets.ModelViewSet):
    """
    A viewset that provides the API related to Operator on-boarding/login
    """
    queryset = UserAuthenticationOTP.objects.all()
    serializer_class = UserOTPGenerationSerializer

    def create(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        operator_obj = Operator.objects.filter(mobile=mobile).first()
        if not operator_obj:
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='User doesn\'t exist.')

        else:
            # Invalidate previous OTPs
            UserOTPGenerationSerializer.invalidate_otp(mobile)

        serializer = UserOTPGenerationSerializer(data=request.data)

        if serializer.is_valid():
            new_otp_created, otp = OTPService().resend_otp(mobile)
            user_obj = operator_obj.user

            # Sending otp through msg91
            template_id = MSG91_TEMPLATE_IDS['SEND_OTP']
            variable_list = [otp, ""]
            msg_sent = MSG91Service(
                mobile, template_id, variable_list).send_sms()

            if not msg_sent:
                send_otp(user_obj, mobile, otp)
                print("Msg sent using TextLocal Service")
            else:
                print("Msg sent using MSG91 Service")

            apnibus_logger.info(otp, mobile)
            if new_otp_created:
                serializer.save(user=user_obj, otp=otp)
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful')

        else:
            return send_response(status=status.HTTP_200_OK, error=serializer.errors,
                                 developer_message='Request failed due to invalid data.')

    @action(methods=['put'], detail=True)
    def verify(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        apnibus_logger.info(mobile, otp)
        valid_otp = UserAuthenticationOTP.objects.filter(mobile=mobile, otp=otp, is_valid=True,
                                                         is_verified=False).first()

        if valid_otp:
            operator_obj = Operator.objects.filter(contact=mobile).first()
            user = operator_obj.user
            if not user:
                user = User.objects.create(
                    username=uuid.uuid1(), user_type=User.OPERATOR)
                operator_obj.user = user
                operator_obj.save()
            token_obj, is_created = Token.objects.get_or_create(user=user)
            auth_token = token_obj.key

            data = {}
            data['auth_token'] = auth_token
            user.is_active = True
            user.save()
            valid_otp.is_valid = False
            valid_otp.is_verified = True
            valid_otp.save()

            return send_response(status=status.HTTP_200_OK, ui_message='message',
                                 developer_message='Request was successful.', data=data)
        return send_response(status=status.HTTP_401_UNAUTHORIZED,
                             developer_message='Invalid otp or mobile number')


class CreateOperatorView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    http_method_names = ['get', 'post', 'put', 'delete']
    # lookup_field = 'mobile'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     mobile_number = self.request.data.get('mobile', None)
    #     if mobile_number:
    #         queryset = queryset.filter(mobile=mobile_number)
    #     return queryset

    # def update(self, request, *args, **kwargs):
    #     mobile_number = self.request.data.get('mobile', None)
    #     instance = self.get_object()
    #     if mobile_number and instance.mobile == mobile_number:
    #         serializer = self.get_serializer(
    #             instance, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.perform_update(serializer)
    #         return Response(serializer.data)
    #     else:
    #         return Response({'detail': 'Invalid mobile number'}, status=status.HTTP_400_BAD_REQUEST)
