from rest_framework import serializers

from account.models.sales_team import SalesTeamUser


class SalesTeamDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTeamUser
        fields = ('id', 'otp', 'name', 'mobile', 'team_type')