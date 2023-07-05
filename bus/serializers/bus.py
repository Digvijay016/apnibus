from rest_framework import serializers
from account.settings.base import BASE_DIR
from utils.serializers import DynamicFieldsModelSerializer
from bus.models.bus import Bus


class BusSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Bus
        fields = ('id', 'bus_number', 'operator', 'pos_serial_no',
                  'pos_dsn_number', 'gps_sim_image')#,'from_town','to_town','start_time','arrival_time','via')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if 'pos_serial_no' in representation and representation['pos_serial_no'] is not None:
            modified_url = representation['pos_serial_no'].replace('http://localhost:8000/media/', '').replace('%3A', ':').replace('https:/', 'https://').replace('%20', ' ')
            print(modified_url)
            representation['pos_serial_no'] = modified_url

        if 'gps_sim_image' in representation and representation['gps_sim_image'] is not None:
            modified_url = representation['gps_sim_image'].replace('http://localhost:8000/media/', '').replace('%3A', ':').replace('https:/', 'https://').replace('%20', ' ')
            print(modified_url)
            representation['gps_sim_image'] = modified_url

        return representation
