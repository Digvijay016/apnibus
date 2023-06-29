# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from account.models.operators import Operator
# import uuid


# @receiver(pre_save, sender=Operator)
# def pre_save_callback(sender, instance, **kwargs):
#     instance.field = "modified value"

#     # Check if the Operator instance already has a user
#     if not instance.user:
#         # Generate a UUID value for the username
#         uuid_value = uuid.uuid4()

#         # Create a new User instance
#         user = User.objects.create_user(
#             username=uuid_value,
#             user_type=User.OPERATOR
#         )

#         # Assign the created User instance to the user field of Operator
#         instance.user = user

#     # Print instance and user
#     print('Instance:', instance)
#     print('User:', instance.user)
# pre_save_callback.connect(pre_save_callback, sender=Operator)

# @receiver(post_save, sender=Operator)
# def post_save_callback(sender, instance, created, **kwargs):
#     if created:
#         # Perform operations after creating a new instance
#         print('######### 1',instance)
#         print('######### 2',created)
#         # adhar_front_img = request.data.get('aadhar_front_photo')
#         # adhar_back_img = request.data.get('aadhar_back_photo')
#         # pan_img = request.data.get('pan_photo')
#         # adhar_front_link, _ = UploadAssetsToS3View.create(
#         #     self, adhar_front_img, 'operator/'+mobile)
#         # adhar_back_link, _ = UploadAssetsToS3View.create(self, adhar_back_img,'operator/'+mobile)
#         # pan_link, _ = UploadAssetsToS3View.create(self, pan_img,'operator/'+mobile)

#         # request.data['aadhar_front_photo'] = str(adhar_front_link)
#         # request.data['aadhar_back_photo'] = str(adhar_back_link)
#         # request.data['pan_photo'] = str(pan_link)
#         pass
#     else:
#         # Perform operations after updating an existing instance
#         pass
