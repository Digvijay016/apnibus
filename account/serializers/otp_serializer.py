from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from rest_framework import serializers
from account.models.user_authentication import UserAuthenticationOTP


class OTPGenerationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=False)

    class Meta:
        model = UserAuthenticationOTP
        fields = ('mobile', 'otp')

    def create(self, validated_data):
        otp_auth = UserAuthenticationOTP.objects.create(**validated_data)
        return otp_auth

    @staticmethod
    def generate_otp():
        return get_random_string(length=4, allowed_chars='1234567890')

    @staticmethod
    def invalidate_otp(mobile):
        prev_5_mins = datetime.now() - timedelta(minutes=5)
        UserAuthenticationOTP.objects.filter(mobile=mobile, created_on__lte=prev_5_mins).update(is_valid=False)


class UserOTPGenerationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=False)

    class Meta:
        model = UserAuthenticationOTP
        fields = ('mobile', 'otp')

    def create(self, validated_data):
        otp_auth = UserAuthenticationOTP.objects.create(**validated_data)
        return otp_auth

    @staticmethod
    def generate_otp():
        return get_random_string(length=4, allowed_chars='1234567890')

    @staticmethod
    def invalidate_otp(mobile):
        prev_5_mins = datetime.now() - timedelta(minutes=5)
        UserAuthenticationOTP.objects.filter(mobile=mobile, created_on__lte=prev_5_mins).update(is_valid=False)