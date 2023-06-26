# from account.models.pos_device import PosDevice
# from booking.models.ticket import TicketDetail
# from operators.models.operator_payment import OperatorInvoice
from rest_framework import serializers
# from account.models import ConductorSE
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Min

# from utils.serializers import DynamicFieldsModelSerializer
from bus.models import Bus
from datetime import date, timedelta


class SalesTeamDataSerializer(serializers.ModelSerializer):
    # booking_status = serializers.SerializerMethodField()
    # payment_status = serializers.SerializerMethodField()
    operator_detail = serializers.SerializerMethodField()
    # pos_detail = serializers.SerializerMethodField()

    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    # buses_in_yesterday_tickets = TicketDetail.objects.filter(created_on__date=yesterday_date).values_list('bus', flat=True)

    class Meta:
        model = Bus
        fields = ('id', 'created_on', 'number', 'gps_status', 'pos_lock', 'conductor_contact',
                  'conductor_name', 'booking_status', 'payment_status', 'operator_detail', 'pos_detail')

    def get_booking_status(self, obj):
        return obj.id in self.buses_in_yesterday_tickets

    # def get_payment_status(self, obj):
    #     operator_invoice = OperatorInvoice.objects.filter(operator=obj.operator, is_paid=False, is_visible=True)
    #     oldest_invoice_date = operator_invoice.aggregate(oldest_date=Min('date'))['oldest_date']
    #     if oldest_invoice_date is None:
    #         payment_pending = False
    #         payment_pending_from = 0
    #         amount = 0
    #     else:
    #         days_since_oldest_invoice = (timezone.now().date() - oldest_invoice_date).days
    #         amount = operator_invoice.aggregate(total_amount=Sum('payable_amount_with_gst'))['total_amount'] or 0
    #         payment_pending = amount >= 1
    #         payment_pending_from = days_since_oldest_invoice
    #     payment = {"payment_pending": payment_pending, "amount": amount, "payment_pending_from": payment_pending_from}
    #     return payment

    def get_operator_detail(self, obj):
        operator = {'name': obj.operator.owner,
                    'company_name': obj.operator.name, 'mobile': obj.operator.mobile}
        return operator

    # def get_pos_detail(self, obj):
    #     latest_pos_device = PosDevice.objects.filter(bus_id=obj).order_by('-updated_on').first()
    #     if not latest_pos_device:
    #         data = {"dsn_number":"Not Available", "version":"Not Available"}
    #         return data
    #     dsn_number = latest_pos_device.dsn_number
    #     version = latest_pos_device.version
    #     if not dsn_number:
    #         dsn_number = "Not Updated"
    #     if not version:
    #         version = "Version less than 32"

    #     data = {"dsn_number":dsn_number, "version":version}

    #     return data
