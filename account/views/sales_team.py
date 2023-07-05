import uuid

from account.models.master_otp import MasterOTP

# from account.models.conductor_se import ConductorSE

from account.serializers.sales_team import SalesTeamDataSerializer
# from operators.models.operator_payment import OperatorInvoice
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
# from bus.models import Bus
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date, timedelta
# from booking.models.ticket import TicketDetail
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
        internal_user_obj, created = SalesTeamUser.objects.get_or_create(
            mobile=mobile, type=SalesTeamUser.SALES)
        print('################', internal_user_obj)
        if not internal_user_obj:
            mobile_number = request.data.get('mobile_number', None)
            name = request.data.get('name', None)
            internal_user_obj, created = SalesTeamUser.objects.get_or_create(
                mobile=mobile_number, name=name, type=SalesTeamUser.SALES)

            if created:
                user = User.objects.create(
                    username=uuid.uuid1(), user_type=User.INTERNAL_USER)
                token = Token.objects.create(user=user)
                print('################', token)
                internal_user_obj.user = user
                internal_user_obj.save()

                # send_response(status=status.HTTP_200_OK, developer_message="User Created")

            # send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="User already exists")

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

        print('################## ', mobile, otp)

        # db_master_otp = MasterOTP.objects.filter(
        #     otp_type=MasterOTP.CONDUCTOR_SE).last().otp

        db_master_otp = 0000

        ui_message = "Request was successful."

        print("###############")

        if otp == db_master_otp:
            internal_team_user = SalesTeamUser.objects.get(mobile=mobile)
            user = internal_team_user.user
            auth_token = Token.objects.get(user=user).key
            data = {}
            print("#######################",auth_token)
            print("#######################",name)
            print("#######################",internal_team_user.mobile)
            data['auth_token'] = auth_token
            data['name'] = internal_team_user.name
            data['mobile'] = internal_team_user.mobile

            user.is_active = True
            user.save()
            # valid_otp.is_valid = False
            # valid_otp.is_verified = True
            # valid_otp.save()

            return send_response(status=status.HTTP_200_OK,
                                 developer_message='Request was successful.', data=data)
        else:
            valid_otp = UserAuthenticationOTP.objects.filter(mobile=mobile, otp=otp, is_valid=True,
                                                             is_verified=False).first()
            print("########## 1", valid_otp, '#########')
            if valid_otp:
                internal_team_user = SalesTeamUser.objects.get(mobile=mobile)
                user = internal_team_user.user
                print("########## 2", user, '#########')
                auth_token = Token.objects.get(user=user).key
                data = {}
                print("########## 3", auth_token, '#########')
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
