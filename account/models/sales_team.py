import uuid
from django.db import models
from .user import User
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class SalesTeamUser(TimeStampedModel):

    SALES = 'sales'
    MARKETING = 'marketing'

    TYPE = (
        (SALES, 'sales'),
        (MARKETING, 'marketing'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='internal_team_user', null=True)
    name = models.CharField(max_length=50, null=True)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    type = models.CharField(max_length=255, choices=TYPE, default=SALES)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.mobile}"
