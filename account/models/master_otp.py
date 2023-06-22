from django.db import models
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class MasterOTP(TimeStampedModel):
    COMMUTER = "commuter"
    CONDUCTOR = "conductor"
    OPERATOR = "operator"
    CONDUCTOR_SE = "conductor_se"

    OTP_TYPE = (
        (COMMUTER, "commuter"),
        (CONDUCTOR, "conductor"),
        (OPERATOR, "operator"),
        (CONDUCTOR_SE, "conductor_se"),


    )
    otp = models.CharField(max_length=10, null=False)
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE, default=COMMUTER)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.otp} {self.otp_type}"
