# import uuid
# from .user import User
# from .operator import Operator
# from django.db import models
# from utils.models import TimeStampedModel
# from simple_history.models import HistoricalRecords


# class Manager(TimeStampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     operator = models.ForeignKey(Operator, on_delete=models.PROTECT, related_name='operator_manager_user', null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_user', null=True)
#     mobile = models.CharField(max_length=10)
#     history = HistoricalRecords()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['operator', 'mobile'], name='UC_operator_manager_mobile'),
#         ]
