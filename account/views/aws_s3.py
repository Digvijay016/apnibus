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

    def create(self, image_name,mobile, *args, **kwargs):
        time_now = datetime.now()
        # img_file = request.FILES["img_file"]
        img_file = image_name
        file_name = img_file.name
        file_extension = file_name.split(".")[-1]
        file_name = file_name.replace(
            f".{file_extension}", '') + str(time_now) + f".{file_extension}"

        # print("AWS File Name ######### : ", file_name,
        #       settings.AWS_BUCKET_NAME, settings.AWS_IMG_FOLDER)

        with open(f'{file_name}', 'wb+') as destination:
            for chunk in img_file.chunks():
                destination.write(chunk)

        # Upload files
        # UploadFiles().get_file_link('img.png',settings.AWS_IMG_FOLDER)
        UploadFiles().upload_file(file_name, settings.AWS_BUCKET_NAME, settings.AWS_IMG_FOLDER+f'/{mobile}')

        file_link = UploadFiles().get_file_link(file_name, settings.AWS_IMG_FOLDER+f'/{mobile}')
        # print("!!!!!!!!!!!", file_link)
        # return file_link
        os.remove(file_name)

        data = {
            "file_link": file_link
        }

        return file_link,send_response(
            data=data,
            status=status.HTTP_200_OK,
            developer_message="Request was successful"
        )
