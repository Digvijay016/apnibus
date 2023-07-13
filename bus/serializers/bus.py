from rest_framework import serializers
from account.settings.base import BASE_DIR
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus import Bus


class BusSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Bus
        fields = ('id', 'bus_number', 'operator', 'pos_serial_no',
                  'pos_dsn_number', 'gps_sim_image','category','brand','has_wifi','has_power_plug',
                  'is_sanitized','is_air_conditioned','operating_as','driver_name','driver_contact',
                  'conductor_name','conductor_contact','seat_type','layout_type','is_multi_axle',
                  'normal_seats_capacity','single_sleeper_capacity','sharing_sleeper_capacity',
                  'upper_single_sleeper_capacity','upper_sharing_sleeper_capacity','recliner_capacity',
                  'status','gps_status','commission','digital_commission','cash_commission',
                  'is_booking_allowed','is_qr_booking_allowed','is_pos_connected','printing_enabled',
                  'trips_access','print_bus_number','access_password','ticket_header','ticket_footer',
                  'subscription_pending','apply_concession','apply_bus_discount','apply_qr_discount',
                  'show_passenger_in_poc','online_app_booking_commission','qr_booking_commission')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        direc = 'http://13.126.0.170:8080/'
        if 'pos_serial_no' in representation and representation['pos_serial_no'] is not None:
            modified_url = representation['pos_serial_no'].replace(direc, '').replace('%3A', ':').replace('https:/', 'https://').replace('%20', ' ')
            print(modified_url)
            representation['pos_serial_no'] = modified_url

        if 'gps_sim_image' in representation and representation['gps_sim_image'] is not None:
            modified_url = representation['gps_sim_image'].replace(direc, '').replace('%3A', ':').replace('https:/', 'https://').replace('%20', ' ')
            print(modified_url)
            representation['gps_sim_image'] = modified_url

        return representation
