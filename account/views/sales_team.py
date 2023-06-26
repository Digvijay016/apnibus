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
from rest_framework import generics
from utils.apnibus_logger import apnibus_logger
from bus.models import Bus
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
        internal_team_user = SalesTeamUser.objects.filter(
            mobile=mobile).first()
        apnibus_logger.info(internal_team_user)
        if not internal_team_user:
            # Can comment this piece of code if we don't want to create new internal team users from app
            # user = User.objects.create(username=uuid.uuid1(), user_type=User.INTERNAL_TEAM)
            # token = Token.objects.create(user=user)
            # internal_team_user = SalesTeamUser.objects.create(user=user, mobile=mobile, type=user_type)
            return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="User doesn't exist in our DB.")

        else:
            # Invalidate previous OTPs
            UserOTPGenerationSerializer.invalidate_otp(mobile)

        serializer = UserOTPGenerationSerializer(data=request.data)

        if serializer.is_valid():
            new_otp_created, otp = OTPService().resend_otp(mobile)
            user_obj = internal_team_user.user
            send_otp(user_obj, mobile, otp)
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

        db_master_otp = MasterOTP.objects.filter(
            otp_type=MasterOTP.CONDUCTOR_SE).last().otp

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
            # valid_otp.is_valid = False
            # valid_otp.is_verified = True
            # valid_otp.save()

            return send_response(status=status.HTTP_200_OK, ui_message='message',
                                 developer_message='Request was successful.', data=data)
        else:
            valid_otp = UserAuthenticationOTP.objects.filter(mobile=mobile, otp=otp, is_valid=True,
                                                             is_verified=False).first()
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

                return send_response(status=status.HTTP_200_OK, ui_message='message',
                                     developer_message='Request was successful.', data=data)
            return send_response(status=status.HTTP_401_UNAUTHORIZED,
                                 developer_message='Invalid otp or mobile number')


class CreateSalesUser(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        mobile_number = request.data.get('mobile_number', None)
        name = request.data.get('name', None)
        internal_user_obj, created = SalesTeamUser.objects.get_or_create(
            mobile=mobile_number, name=name, type=SalesTeamUser.SALES)

        if created:
            user = User.objects.create(
                username=uuid.uuid1(), user_type=User.INTERNAL_USER)
            token = Token.objects.create(user=user)
            internal_user_obj.user = user
            internal_user_obj.save()

            return send_response(status=status.HTTP_200_OK, developer_message="User Created")

        return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="User already exists")


class SalesTeamDataView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def list(self, request, *args, **kwargs):
    #     user = request.user
    #     buses = Bus.objects.filter(bd__user = user)
    #     total_pos = buses.filter(is_pos_connected = True).count()
    #     gps_not_working = buses.filter(is_pos_connected = True).exclude(gps_status = 'installed').count()
    #     pos_locked = buses.filter(is_pos_connected = True, pos_lock = True).count()

    #     today_date = date.today()
    #     yesterday_date = today_date - timedelta(days=1)
    #     # yesterday_tickets = TicketDetail.objects.filter(created_on__date=yesterday_date, bus__is_pos_connected = True, bus__bd__user = user )
    #     # buses_in_yesterday_tickets = yesterday_tickets.values('bus').distinct().count()
    #     # conductor_not_using_pos = total_pos - buses_in_yesterday_tickets

    #     pending_pyment_count = 0
    #     pos_on_demo = 0
    #     index = 0
    #     opertors = []
    #     for bus in buses.filter(is_pos_connected = True):
    #         index +=1
    #         operator_invoice = OperatorInvoice.objects.filter(operator=bus.operator, is_visible=True)
    #         paid_invoice = operator_invoice.filter(is_paid=True).aggregate(total_amount=Sum('payable_amount_with_gst'))['total_amount'] or 0
    #         print(index, paid_invoice)
    #         if paid_invoice == 0:
    #             pos_on_demo = pos_on_demo + 1

    #         unpaid_invoice = operator_invoice.filter(is_paid=False)
    #         amount = unpaid_invoice.aggregate(total_amount=Sum('payable_amount_with_gst'))['total_amount'] or 0
    #         if amount >= 1:

    #             if bus.operator not in opertors:
    #                 opertors.append(bus.operator)
    #                 pending_pyment_count = pending_pyment_count + amount
    #     current_month = timezone.now().month
    #     current_year = timezone.now().year
    #     this_month_sale = buses.filter(created_on__month=current_month,is_pos_connected = True , created_on__year=current_year).count()

    #     data = {
    #         'buses': buses.count(),
    #         'total_pos': total_pos,
    #         'gps_not_working': gps_not_working,
    #         'conductor_not_using_pos':conductor_not_using_pos,
    #         'pos_locked':pos_locked,
    #         'this_month_sale':this_month_sale,
    #         'pending_pyment_count':pending_pyment_count,
    #         'pos_on_demo':pos_on_demo
    #     }

    #     print(buses)

    #     return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
    #                          data=data)


class SalesTeamDataDetialView(generics.ListAPIView):
    serializer_class = SalesTeamDataSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        total_buses = request.GET.get('total_buses', None)
        total_pos = request.GET.get('total_pos', None)
        gps_not_working = request.GET.get('gps_not_working', None)
        conductor_not_using_pos = request.GET.get(
            'conductor_not_using_pos', None)
        pos_locked = request.GET.get('pos_locked', None)
        this_month_sale = request.GET.get('this_month_sale', None)
        # pending_pyment = request.GET.get('pending_pyment', None)
        # pos_on_demo = request.GET.get('pos_on_demo', None)
        bus = request.GET.get('bus_id', None)

        user = request.user
        queryset = Bus.objects.filter(bd__user=user, is_pos_connected=True)

        if bus:
            queryset = Bus.objects.filter(bd__user=user, id=bus)

        if total_buses:
            queryset = Bus.objects.filter(bd__user=user)
        if total_pos:
            queryset = queryset
        if gps_not_working:
            queryset = queryset.filter(
                is_pos_connected=True).exclude(gps_status='installed')
        if conductor_not_using_pos:
            today_date = date.today()
            yesterday_date = today_date - timedelta(days=1)
            # yesterday_tickets = TicketDetail.objects.filter(created_on__date=yesterday_date, bus__is_pos_connected = True )
            # yesterday_pos_using_bus_list = yesterday_tickets.values_list('bus', flat=True).distinct()
            # queryset = queryset.exclude(id__in=yesterday_pos_using_bus_list)
        if pos_locked:
            queryset = queryset.filter(pos_lock=True)
        if this_month_sale:
            current_month = timezone.now().month
            current_year = timezone.now().year
            queryset = queryset.filter(
                created_on__month=current_month, created_on__year=current_year)

        # if pending_pyment or pos_on_demo:
        #     operator_invoice = OperatorInvoice.objects.filter(is_visible=True)
        #     paid_invoice = operator_invoice.filter(is_paid=True).aggregate(total_amount=Sum('payable_amount_with_gst'))['total_amount'] or 0
        #     if paid_invoice == 0:
        #         if pos_on_demo:
        #             operator_ids = operator_invoice.filter(is_paid=True).values_list('operator', flat=True)
        #             queryset = queryset.filter(is_pos_connected = True).exclude(operator__in=operator_ids)

        #     unpaid_invoice = operator_invoice.filter(is_paid=False)
        #     amount = unpaid_invoice.aggregate(total_amount=Sum('payable_amount_with_gst'))['total_amount'] or 0
        #     if amount >= 1:
        #         if pending_pyment:
        #             operator_ids = unpaid_invoice.values_list('operator', flat=True)
        #             queryset = queryset.filter(operator__in=operator_ids)

        # if pending_pyment:
        #     operator_ids = OperatorInvoice.objects.filter(is_visible=True, is_paid=False).values_list('operator', flat=True)
        #     queryset = queryset.filter(operator__in=operator_ids)

        # if pos_on_demo:
        #     operator_ids = OperatorInvoice.objects.filter(is_visible=True, is_paid=True).values_list('operator', flat=True)
        #     queryset = queryset.exclude(operator__in=operator_ids)

        data = self.get_serializer(queryset, many=True).data
        # sort the data by payment_pending and booking_status
        return send_response(status=status.HTTP_200_OK, developer_message='Request was successful.',
                             data=data)
