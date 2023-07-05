from utils.sms_service import SMSService
from datetime import datetime, timedelta
from django.utils import timezone
from account.models.user_authentication import UserAuthenticationOTP
from account.serializers.otp_serializer import OTPGenerationSerializer, UserOTPGenerationSerializer


class OTPService():
    """
    This class contains methods related to OTP.
    """

    @classmethod
    def send_otp(cls, mobile, otp, message):

        mobile_number = mobile
        otp_request = SMSService(mobile_number, message).send_sms()
        return otp_request

    @classmethod
    def verify_otp(cls, mobile_number, otp):
        otp_auth_object = UserAuthenticationOTP.objects.filter(mobile_number=mobile_number,
                                                               otp=otp, is_deleted=False,
                                                               is_valid=True).first()

        if not otp_auth_object:
            return False, "Request failed due to Invalid OTP or mobile number"

        else:
            if cls.check_validity(otp_auth_object):
                otp_auth_object.is_valid = False
                otp_auth_object.is_verified = True
                otp_auth_object.save()
                return True, "Request was Successful"

            return False, "Request failed due to Invalid OTP"

    @classmethod
    def resend_otp(cls, mobile):

        new_otp_created = False
        mobile_number = mobile
        otp_exists = UserAuthenticationOTP.objects.filter(
            mobile=mobile_number, is_valid=True, is_deleted=False).first()
        if otp_exists:
            validity = cls.check_validity(otp_exists)
            if validity:
                otp = otp_exists.otp
                return new_otp_created, otp

            else:
                new_otp_created = True
                otp = OTPGenerationSerializer.generate_otp()
                return new_otp_created, otp

        else:
            new_otp_created = True
            otp = OTPGenerationSerializer.generate_otp()
            return new_otp_created, otp

    @classmethod
    def check_validity(cls, instance):
        validity_period = timedelta(minutes=5)
        now = timezone.now()
        if now - instance.created_on < validity_period:
            return True
        else:
            instance.is_valid = False
            instance.save()
            return False


class UserOTPService():

    @classmethod
    def send_otp(cls, mobile, otp, message):

        mobile_number = mobile
        otp_request = SMSService(mobile_number, message).send_sms()
        return otp_request

    @classmethod
    def verify_otp(cls, mobile_number, otp):
        otp_auth_object = UserAuthenticationOTP.objects.filter(mobile=mobile_number,
                                                               otp=otp, is_deleted=False,
                                                               is_valid=True).first()

        if not otp_auth_object:
            return False, "Request failed due to Invalid OTP or mobile number"

        else:
            if cls.check_validity(otp_auth_object):
                otp_auth_object.is_valid = False
                otp_auth_object.is_verified = True
                otp_auth_object.save()
                return True, "Request was Successful"

            return False, "Request failed due to Invalid OTP"

    @classmethod
    def resend_otp(cls, mobile):

        new_otp_created = False
        mobile_number = mobile
        otp_exists = UserAuthenticationOTP.objects.filter(
            mobile=mobile_number, is_valid=True, is_deleted=False).first()
        if otp_exists:
            validity = cls.check_validity(otp_exists)
            if validity:
                otp = otp_exists.otp
                return new_otp_created, otp

            else:
                new_otp_created = True
                otp = UserOTPGenerationSerializer.generate_otp()
                return new_otp_created, otp

        else:
            new_otp_created = True
            otp = UserOTPGenerationSerializer.generate_otp()
            return new_otp_created, otp

    @classmethod
    def check_validity(cls, instance):
        validity_period = timedelta(minutes=5)
        if datetime.now(timezone.utc) - instance.created_on < validity_period:
            return True
        else:
            instance.is_valid = False
            instance.save()
            return False
