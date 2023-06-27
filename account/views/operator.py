from ast import operator
from distutils.command.upload import upload
import uuid
from django.db import transaction
from rest_framework import viewsets, status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from account.helpers.otp import send_otp
from account.helpers.otp_service import OTPService
from account.serializers.commuter import UserOTPGenerationSerializer
from account.models.operators import Operator
from account.views.aws_s3 import UploadAssetsToS3View
# from utils.aws_s3 import UploadFiles
from utils.restful_response import send_response
from account.models.user_authentication import UserAuthenticationOTP
from account.models.user import User
from account.serializers.operator import OperatorSerializer
from account.pagination import AccountListPagination
from utils.apnibus_logger import apnibus_logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.sms_service import MSG91_TEMPLATE_IDS, MSG91Service
from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()


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


class CreateOperatorView(generics.CreateAPIView):
    serializer_class = OperatorSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        operator_exists = Operator.objects.filter(mobile=mobile).exists()

        # email = request.data.pop('email', None)
        # print('Email ------ ',request.data)
        # bank_accounts = request.data.pop('bank_accounts', [])
        # print("$$$$$$$$$$$ ",request.FILES.get('pan_photo'))
        # pan_img = request.FILES.get('pan_photo')
        adhar_front_img = request.data.get('aadhar_front_photo')
        adhar_back_img = request.data.get('aadhar_back_photo')
        pan_img = request.data.get('pan_photo')
        adhar_front_link, _ = UploadAssetsToS3View.create(
            self, adhar_front_img, 'operator/'+'mobile-'+mobile)
        adhar_back_link, _ = UploadAssetsToS3View.create(self, adhar_back_img,'operator/'+'mobile-'+mobile)
        pan_link, _ = UploadAssetsToS3View.create(self, pan_img,'operator/'+'mobile-'+mobile)

        request.data['aadhar_front_photo'] = str(adhar_front_link)
        request.data['aadhar_back_photo'] = str(adhar_back_link)
        request.data['pan_photo'] = str(pan_link)

        # print(adhar_front_link)
        # print(adhar_back_link)
        # print(pan_link)

        # operator_instance = Operator()
        # operator_instance.aadhar_front_photo.upload_to = adhar_front_link
        # operator_instance.aadhar_front_photo.upload_to = adhar_back_link
        # operator_instance.aadhar_front_photo.upload_to = pan_link
        # operator_instance.save()
        # print("@@@@@@@@@@@", operator_instance.aadhar_front_photo.upload_to)

        # operator.file.aadhar_front_photo.upload_to = UploadFiles.get_file_link(self,adhar_front_img, settings.AWS_IMG_FOLDER)
        # operator.file.aadhar_back_photo.upload_to = UploadFiles.get_file_link(self,adhar_back_img, settings.AWS_IMG_FOLDER)
        # operator.file.pan.upload_to = UploadFiles.get_file_link(self,pan_img, settings.AWS_IMG_FOLDER)
        # file_link = UploadAssetsToS3View.create(self,pan_img)
        # print("############## ",file_link)

        if operator_exists:
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.',
                                 ui_message='Operator already exists with this mobile')
        uuid_value = uuid.uuid4()
        user = User.objects.create_user(
            username=uuid_value, user_type=User.OPERATOR)
        # user.save()

        print("######### 1 ##########", user)

        token = Token.objects.create(user=user)
        # token.save()

        print('Token generated ---------- ', token)
        # upload_files = UploadFiles

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=user)
            # a_f = instance.aadhar_front_photo.url.replace('http://localhost:8000/', '').replace('%3A', ':/')
            # a_b = instance.aadhar_back_photo.url.replace('http://localhost:8000/', '').replace('%3A', ':/')
            # pan = instance.pan_photo.url.replace('http://localhost:8000/', '').replace('%3A', ':/')

            # instance.aadhar_front_photo = a_f
            # instance.aadhar_back_photo = a_b
            # instance.pan_photo = pan
            # print("!!!!!!!!! ", serializer.data.get('aadhar_front_photo'))
            # a_f = serializer.data.get(
            #     'aadhar_front_photo').replace('http://localhost:8000/', '')
            # a_f = a_f.replace('%3A', ':/')
            # a_b = serializer.data.get(
            #     'aadhar_back_photo').replace('http://localhost:8000/', '')
            # a_b = a_b.replace('%3A', ':/')
            # pan = serializer.data.get(
            #     'pan_photo').replace('http://localhost:8000/', '')
            # pan = pan.replace('%3A', ':/')
            # serializer.data['aadhar_front_photo'] = str(a_f)
            # serializer.data['aadhar_back_photo'] = str(a_b)
            # serializer.data['pan_photo'] = str(pan)
            # print(serializer.data['aadhar_front_photo'])
            # print(serializer.data['aadhar_back_photo'])
            # print(serializer.data['pan_photo'])
            # print(instance.aadhar_front_photo)
            # print(instance.aadhar_back_photo)
            # print(instance.pan_photo)
            data = self.get_serializer(instance).data
            return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                                 data=data)
        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message='Request failed.', ui_message='Invalid data', error=serializer.errors)


class OperatorListView(generics.ListAPIView):
    serializer_class = OperatorSerializer
    queryset = Operator.objects.all()
    pagination_class = AccountListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # queryset = queryset/
        # print("Checking----------",queryset)
        # name = request.GET.get('name', None)
        # owner = request.GET.get('owner', None)
        # mobile = request.GET.get('mobile', None)
        #
        # if mobile:
        #     queryset = queryset.filter(mobile__icontains=mobile).order_by('mobile')
        #
        # if name:
        #     queryset = queryset.filter(name__icontains=name).order_by('name')
        #
        # if owner:
        #     queryset = queryset.filter(owner__icontains=owner).order_by('owner')

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=response.data)


class OperatorUpdateView(generics.UpdateAPIView):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        apnibus_logger.info(request.data)
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                operator_email = request.data.get('email', None)

                if operator_email:
                    operator_serializer = serializer.save()
                    operator_serializer.user.email = operator_email
                    operator_serializer.user.save()
                    operator_serializer.save()

                operator_status = request.data.get('status', None)
                if operator_status:
                    operator_serializer = serializer.save()
                    if operator_status == Operator.DEBOARDED:
                        operator_serializer.subscription_pending = True
                        operator_serializer.save()
                    if operator_status == Operator.ONBOARDED:
                        operator_serializer.subscription_pending = False
                        operator_serializer.save()
                    if operator_status == Operator.LOCKED:
                        operator_serializer.subscription_pending = True
                        operator_serializer.save()

                operator_serializer = serializer.save()

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
                data = self.get_serializer(operator_serializer).data
                return send_response(status.HTTP_200_OK, data=data, developer_message='Request was successful.')

        return send_response(status=status.HTTP_400_BAD_REQUEST, error=serializer.errors,
                             developer_message='Request failed due to invalid data.')


class OperatorRetrieveView(generics.RetrieveAPIView):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # print('Instance ---- ',instance)
        except Exception as e:
            return send_response(status.HTTP_400_BAD_REQUEST,
                                 developer_message='Request has failed because of invalid bus_number',
                                 ui_message='The bus_number you\'re tyring to access does not exist')
        serializer = self.get_serializer(instance)
        return send_response(status.HTTP_200_OK, data=serializer.data,
                             developer_message='Request was success')


class OperatorSearchView(generics.ListAPIView):
    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        name = request.GET.get('name', None)
        owner = request.GET.get('owner', None)
        mobile = request.GET.get('mobile', None)
        # print('Search name ---- ', name)
        # print('Search owner ---- ', owner)
        # print('Search mobile ---- ', mobile)
        # # searchParam = self.kwargs['name']
        # print('Kwargs value ---- ', **kwargs)
        # print('Query Set ----- ',queryset)
        # print('Kwargs value ---- ', searchParam)
        # instance = self.get_object()
        # print('Instance ---- ', instance)
        # print('Request ---- ', request)
        if mobile:
            queryset = queryset.filter(
                mobile__icontains=mobile).order_by('mobile')

        if name:
            queryset = queryset.filter(name__icontains=name).order_by('name')

        if owner:
            queryset = queryset.filter(
                owner__icontains=owner).order_by('owner')

        fields = ('id', 'name', 'mobile', 'owner', 'bus_count')
        data = self.get_serializer(queryset, many=True, fields=fields).data
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)
