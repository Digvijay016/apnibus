import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords


class User(AbstractUser, TimeStampedModel):

    ADMIN = 'admin'
    CONDUCTOR = 'conductor'
    BUS_DRIVER = 'bus_driver'
    COMMUTER = 'commuter'
    INTERNAL_USER = 'internal_user'
    OPERATOR = 'operator'
    POS_DEVICE = 'pos_device'
    CONDUCTOR_SE = 'conductor_se'
    OPERATOR_SALES_LEAD = 'operator_sales_lead'
    SALES = 'Sales'

    USER_TYPE = (
        (ADMIN, 'admin'),
        (CONDUCTOR, 'conductor'),
        (COMMUTER, 'commuter'),
        (INTERNAL_USER, 'internal_user'),
        (OPERATOR, 'operator'),
        (BUS_DRIVER, 'bus_driver'),
        (POS_DEVICE, 'pos_device'),
        (CONDUCTOR_SE, 'conductor_se'),
        (OPERATOR_SALES_LEAD, 'operator_sales_lead'),
        (SALES, 'Sales')
    )

    ENGLISH = "english"
    HINDI = "hindi"

    PREFERRED_LANGUAGES = (
        (ENGLISH, 'english'),
        (HINDI, 'hindi'),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for the user.',
        related_name='user_permissions_user'  # Add a unique related_name
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups'  # Add a unique related_name
    )

    class Meta:
        app_label = 'account'

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user_type = models.CharField(max_length=25, choices=USER_TYPE)
    preferred_language = models.CharField(
        max_length=255, choices=PREFERRED_LANGUAGES, default=ENGLISH)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.username)
