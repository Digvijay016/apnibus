# from rest_framework import generics, status
# from rest_framework.authtoken.models import Token
# from utils.restful_response import send_response
# from account.models import User, AdminUser


# class LoginAdminUser(generics.CreateAPIView):
#     """
#     working: Using this API to create user in AdminUser table and to retrieve token for already existing users.
#     """

#     def create(self, request, *args, **kwargs):
#         user_email = request.data.get('user_email', None)
#         display_name = request.data.get('display_name', None)
#         add_new_user = request.data.get('add_new_user', False)
#         user_role = request.data.get('user_role', AdminUser.EDITOR)

#         user = User.objects.filter(username=user_email, user_type=User.ADMIN).first()
#         if not user:
#             if add_new_user:
#                 user = User.objects.create(username=user_email, user_type=User.ADMIN)
#                 admin_user = AdminUser.objects.create(user=user, display_name=display_name, role=user_role)
#                 auth_token = Token.objects.create(user=user).key

#             auth_token = None

#         else:
#             auth_token = Token.objects.get(user=user).key
#             user_role = user.admin_user.role

#         data = {'auth_token': auth_token, 'role': user_role}

#         return send_response(status=status.HTTP_200_OK, ui_message="Request was successful.",
#                              developer_message='Request was successful.', data=data)

