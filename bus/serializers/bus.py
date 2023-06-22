from rest_framework import serializers
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus import Bus
# from account.serializers import OperatorSerializer
# from bus.helpers.translate_attribute import translate_attribute
# from account.models import User
# from operators.models import OperatorRemark
# from operators.serializers import OperatorRemarkSerializer


class BusSerializer(DynamicFieldsModelSerializer):
    # operator = OperatorSerializer(required=False)
    # remarks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bus
        fields = ('id', 'bus_number', 'pos_serial_no', 'pos_dsn_number', 'gps_sim_image')

    # def __init__(self, *args, **kwargs):
        # super(BusSerializer, self).__init__(*args, **kwargs)
        # is_list = self.context.get('is_list', False)
        # if is_list:
        # self.fields = ('bus_number',)

    # def get_remarks(self, obj):
    #     qs = OperatorRemark.objects.filter(bus=obj)
    #     serializer_data = OperatorRemarkSerializer(qs, many=True).data
    #     return serializer_data


# class BusResponseSerializer(DynamicFieldsModelSerializer):
#     operator = OperatorSerializer(required=False)
#     category = serializers.SerializerMethodField()
#     seat_type = serializers.SerializerMethodField()
#     remarks = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = Bus
#         fields = ('id', 'operator', 'number', 'category', 'brand', 'has_wifi', 'has_power_plug', 'is_sanitized',
#                   'is_air_conditioned', 'operating_as', 'driver_name', 'conductor_name', 'driver_contact',
#                   'conductor_contact',
#                   'seat_type', 'normal_seats_capacity', 'single_sleeper_capacity', 'sharing_sleeper_capacity',
#                   'layout_type', 'is_multi_axle', 'status', 'gps_status', 'commission', 'is_booking_allowed',
#                   'is_pos_connected', 'printing_enabled', 'trips_access', 'access_password', 'remarks')
#
#     def __init__(self, *args, **kwargs):
#         super(BusSerializer, self).__init__(*args, **kwargs)
#         is_list = self.context.get('is_list', False)
#         if is_list:
#             self.fields.pop('address')
#             self.fields.pop('gstin')
#             self.fields.pop('aadhar_number')
#             self.fields.pop('pan_number')
#             self.fields.pop('bank_accounts')
#             self.fields = ('number',)
#
#     def get_category(self, obj):
#         category = obj.category
#         preferred_language = self.context.get('preferred_language', User.ENGLISH).lower()
#         category = translate_attribute(category, preferred_language)
#         return category
#
#     def get_seat_type(self, obj):
#         seat_type = obj.seat_type
#         preferred_language = self.context.get('preferred_language', User.ENGLISH).lower()
#         seat_type = translate_attribute(seat_type, preferred_language)
#         return seat_type
#
#     def get_remarks(self, obj):
#         qs = OperatorRemark.objects.filter(bus=obj)
#         serializer_data = OperatorRemarkSerializer(qs, many=True).data
#         return serializer_data
#
#
# class BusPhotographSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BusPhotograph
#         fields = ('id', 'bus_image_id', 'bus', 'type', 'image')