from django.db import models
# from account.models.sales_team import SalesTeamUser
# from rest_framework import status
# from account.helpers.otp import send_otp
# from account.models.sales_team import SalesTeamUser
from account.models.user import User
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from account.helpers.otp_service import OTPService
# from utils.restful_response import send_response


class UserAuthenticationOTP(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    mobile = models.CharField(max_length=10)
    # email = models.EmailField(unique=True, default='abc@gmail.com')
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.user, self.otp)

    # @staticmethod
    # @receiver(post_save, sender='account.UserAuthenticationOTP')
    # def post_save_callback(sender, instance, created, **kwargs):
    #     from account.serializers.commuter import UserOTPGenerationSerializer
    #     mobile = instance.mobile
    #     internal_team_user = SalesTeamUser.objects.filter(
    #         mobile=mobile).first()

    #     if not internal_team_user:
    #         return send_response(status=status.HTTP_400_BAD_REQUEST, developer_message="User doesn't exist in our DB.")
    #     else:
    #         # Invalidate previous OTPs
    #         UserOTPGenerationSerializer.invalidate_otp(mobile)

    #     serializer = UserOTPGenerationSerializer(data=instance)

    #     if serializer.is_valid():
    #         new_otp_created, otp = OTPService().resend_otp(mobile)
    #         print("########### 1", new_otp_created, otp)
    #         user_obj = internal_team_user.user
    #         send_otp(user_obj, mobile, otp)
    #         if new_otp_created:
    #             serializer.save(user=user_obj, otp=otp)
    #             instance.save()
