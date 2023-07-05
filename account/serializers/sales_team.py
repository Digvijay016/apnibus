from rest_framework import serializers

from account.models.sales_team import SalesTeamUser


class SalesTeamDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTeamUser
        # fields = ('id', 'created_on', 'number', 'gps_status', 'pos_lock', 'conductor_contact',
        #           'conductor_name', 'booking_status', 'payment_status', 'operator_detail', 'pos_detail')
        fields = ('id', 'user', 'name', 'mobile', 'email', 'type')