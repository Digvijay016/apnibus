# import uuid
# from django.db import models
# from .user import User
# from utils.models import TimeStampedModel


# class AdminUser(TimeStampedModel):
#     SUPER_ADMIN = "super_admin"
#     EDITOR = "editor"
#     ACCOUNTANT = "accountant"
#     SUPPORT = "support"
#     ACCOUNTANT_AND_EDITOR = "accountant_and_editor"
#     OWNER = 'owner'

#     USER_ROLES = (
#         (SUPER_ADMIN, "super_admin"),
#         (EDITOR, "editor"),
#         (ACCOUNTANT,  "accountant"),
#         (SUPPORT, "support"),
#         (ACCOUNTANT_AND_EDITOR, "accountant_and_editor"),
#         (OWNER, 'owner')
#     )

#     id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     display_name = models.CharField(max_length=255, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='admin_user')
#     role = models.CharField(max_length=255, choices=USER_ROLES, default=EDITOR)
