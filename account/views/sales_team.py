import uuid

from account.models.master_otp import MasterOTP

from account.serializers.sales_team import SalesTeamDataSerializer
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from account.helpers.otp import send_otp
from account.helpers.otp_service import OTPService
from account.serializers.commuter import UserOTPGenerationSerializer
from utils.restful_response import send_response
from account.models.user_authentication import UserAuthenticationOTP
from account.models.sales_team import SalesTeamUser
from account.models.user import User
from rest_framework import viewsets, generics
from utils.apnibus_logger import apnibus_logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta
from django.db.models import Sum
from django.utils import timezone


class UserAuthOTPViewset(viewsets.ModelViewSet):
    """
    A viewset that provides the API related to SalesTeamUser on-boarding/ login
    """
    queryset = UserAuthenticationOTP.objects.all()
    serializer_class = UserOTPGenerationSerializer

    def create(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', None)
        internal_user_obj = SalesTeamUser.objects.filter(
            mobile=mobile, type=SalesTeamUser.SALES).first()

        if not mobile.isnumeric() or len(mobile) != 10:
            error = 'Invalid mobile number.Mobile number must be of 10 digits.'
            return send_response(status=status.HTTP_200_OK, error_msg=error,
                                 developer_message='Request failed due to invalid data.')

        if not internal_user_obj:
            mobile_number = request.data.get('mobile', None)
            name = request.data.get('name', None)
            internal_user_obj, created = SalesTeamUser.objects.get_or_create(
                mobile=mobile_number, name=name, type=SalesTeamUser.SALES)

            if created:
                user = User.objects.create(
                    username=uuid.uuid1(), user_type=User.SALES)
                token = Token.objects.create(user=user)
                internal_user_obj.user = user
                internal_user_obj.save()

        else:
            # Invalidate previous OTPs
            UserOTPGenerationSerializer.invalidate_otp(mobile)

        serializer = UserOTPGenerationSerializer(data=request.data)

        if serializer.is_valid():
            new_otp_created, otp = OTPService().resend_otp(mobile)
            user_obj = internal_user_obj.user
            send_otp(user_obj, mobile, otp)
            apnibus_logger.info(otp, mobile)
            if new_otp_created:
                serializer.save(user=user_obj, otp=otp)
            return send_response(status=status.HTTP_200_OK, error_msg={}, developer_message='Request was successful', response_message='Success')

        else:
            return send_response(status=status.HTTP_200_OK, error=serializer.errors,
                                 developer_message='Request failed due to invalid data.', response_message='Error')

    @action(methods=['put'], detail=False)
    def verify(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        apnibus_logger.info(mobile, otp)

        db_master_otp = 0000

        ui_message = "Request was successful."

        if otp == db_master_otp:
            internal_team_user = SalesTeamUser.objects.get(mobile=mobile)
            user = internal_team_user.user
            auth_token = Token.objects.get(user=user).key
            data = {}
            data['auth_token'] = auth_token
            data['name'] = internal_team_user.name
            data['mobile'] = internal_team_user.mobile

            user.is_active = True
            user.save()
            valid_otp.is_valid = False
            valid_otp.is_verified = True
            valid_otp.save()

            return send_response(status=status.HTTP_200_OK,
                                 developer_message='Request was successful.', data=data)
        else:
            valid_otp = UserAuthenticationOTP.objects.filter(mobile=mobile, otp=otp).first()
            
            if valid_otp:
                internal_team_user = SalesTeamUser.objects.get(mobile=mobile)
                user = internal_team_user.user
                
                auth_token = Token.objects.get(user=user).key
                data = {}
                
                data['auth_token'] = auth_token
                data['name'] = internal_team_user.name
                data['mobile'] = internal_team_user.mobile

                user.is_active = True
                user.save()
                valid_otp.is_valid = False
                valid_otp.is_verified = True
                valid_otp.save()

                return send_response(status=status.HTTP_200_OK, error_msg={},
                                     developer_message='Request was successful.', data=data, response_message='Success')
            return send_response(status=status.HTTP_401_UNAUTHORIZED, error_msg={},
                                 developer_message='Invalid otp or mobile number', response_message='Error')


class CreateSalesUser(viewsets.ModelViewSet):
    queryset = SalesTeamUser.objects.all()
    serializer_class = SalesTeamDataSerializer
