from django.db import models
from utils.models import TimeStampedModel
import uuid
from simple_history.models import HistoricalRecords


class Task(TimeStampedModel):
    ACTIVE = 'a'
    INACTIVE = 'i'

    STATUS = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive')
    )

    SALES = 's'
    MARKETING = 'm'

    TEAM = (
        (SALES,'Sales'),
        (MARKETING,'Marketing')
    )

    HIGH = 'h'
    MEDIUM = 'm'
    LOW = 'l'

    PRIORITY = (
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=255, choices=PRIORITY, default=HIGH, blank=True)
    task = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255,choices=STATUS, default=INACTIVE, blank=True)
    team_type = models.CharField(max_length=20, choices=TEAM, default=SALES, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title}"