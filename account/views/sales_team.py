import uuid

import json
import sys
from account.serializers.sales_team import SalesTeamDataSerializer
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from account.helpers.otp import send_otp
from django.contrib.auth.models import User
from utils.restful_response import send_response
from account.models.sales_team import SalesTeamUser
from rest_framework import viewsets, generics
from utils.apnibus_logger import apnibus_logger
from datetime import date, datetime, timedelta
from utils.sms_service import SMSService


class SalesTeamOTPViewset(viewsets.ModelViewSet):
    """
    A viewset that provides the API related to SalesTeamUser on-boarding/ login
    """

    queryset = SalesTeamUser.objects.all()
    serializer_class = SalesTeamDataSerializer

    def create(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', None)
        internal_user_obj, created = SalesTeamUser.objects.get_or_create(mobile=mobile)
        validity = timezone.now() - internal_user_obj.updated_on.replace(tzinfo=timezone.utc)
        if not created and validity > timedelta(minutes=20):
            internal_user_obj.save()
        try:
            otp_req = send_otp(internal_user_obj, mobile, internal_user_obj.otp)
            return send_response(status=status.HTTP_200_OK, error_msg={},
                    developer_message='Request was successful', response_message='Success')
        except:
            print(sys.exc_info())
        return send_response(status=status.HTTP_200_OK, error='Error in otp creation.',
                developer_message='Request failed due to invalid data.', response_message='Error')

    @action(methods=['put'], detail=False)
    def verify(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        apnibus_logger.info(mobile, otp)
        sales_user = SalesTeamUser.objects.get(mobile=mobile)
        validity = timezone.now() - sales_user.updated_on.replace(tzinfo=timezone.utc)
        if sales_user.otp == otp and validity < timedelta(minutes=20):
            data = {
                    'auth_token': str(sales_user.auth_token),
                    'mobile': str(mobile)
                    }
            
            return send_response(status=status.HTTP_200_OK, error_msg={},
                    developer_message='Request was successful.', data=data, response_message='Success')
        return send_response(status=status.HTTP_401_UNAUTHORIZED, error_msg={},
                developer_message='Invalid otp or mobile number', response_message='Error')

