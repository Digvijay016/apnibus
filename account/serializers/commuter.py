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


class CommuterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", allow_blank=True, required=False)
    email = serializers.CharField(source="user.email", allow_blank=True)
    mobile = serializers.CharField(read_only=True)
    profile_image_url = serializers.SerializerMethodField()
    preferred_language = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'mobile', 'dob', 'first_name', 'last_name', 'email', 'profile_image_url',
                  'preferred_language', 'send_whatsapp_message', 'dnd_whatsapp_message')

    def update(self, instance, validated_data):
        user_data = validated_data.get('user', None)
        if user_data:
            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)
            instance.user.email = user_data.get('email', instance.user.email)
            instance.user.preferred_language = user_data.get('preferred_language', instance.user.preferred_language)

        instance.dob = validated_data.get('dob', instance.dob)
        instance.user.save()
        instance.save()

        return instance

    def get_profile_image_url(self, obj):
        url = "https://apnibus.in"
        return url

    def get_preferred_language(self, obj):
        return obj.user.preferred_language
