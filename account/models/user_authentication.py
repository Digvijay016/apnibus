from django.db import models
from account.models.user import User
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class UserAuthenticationOTP(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    mobile = models.CharField(max_length=10)
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.user, self.otp)

    