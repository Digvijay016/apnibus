import os
from datetime import datetime
from rest_framework import generics, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.restful_response import send_response
from utils.aws_s3 import UploadFiles
from django.conf import settings


class UploadAssetsToS3View(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, image_name, folder_name, *args, **kwargs):
        print('$$$$$$$$$$$$$$ Image Name $$$$$$$$$$$$$$$$', image_name)
        time_now = datetime.now()
        # img_file = request.FILES["img_file"]
        img_file = str(image_name)
        # file_name = img_file.name
        file_extension = img_file.split(".")[-1]
        file_name = img_file.replace(
            f".{file_extension}", '') + str(time_now) + f".{file_extension}"

        with open(f'{file_name}', 'wb+') as destination:
            for chunk in image_name.chunks():
                destination.write(chunk)

        UploadFiles().upload_file(file_name, settings.AWS_BUCKET_NAME,
                                  settings.AWS_IMG_FOLDER+f'/{folder_name}')

        file_link = UploadFiles().get_file_link(
            file_name, settings.AWS_IMG_FOLDER+f'/{folder_name}')
        os.remove(file_name)

        data = {
            "file_link": file_link
        }

        return file_link, send_response(
            data=data,
            status=status.HTTP_200_OK,
            developer_message="Request was successful"
        )
