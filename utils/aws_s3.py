import os
import boto3
from django.conf import settings


class UploadFiles:
    def __init__(self):
        self.AWS_BUCKET_NAME = settings.AWS_BUCKET_NAME
        self.BUCKET_REGION_NAME = settings.BUCKET_REGION_NAME
        self.s3_conn = boto3.client('s3',
                                    aws_access_key_id=settings.AWS_ACCESS_KEY,
                                    aws_secret_access_key=settings.AWS_SECRET_KEY)
        self.base_url = f"https://{self.AWS_BUCKET_NAME}.s3.{self.BUCKET_REGION_NAME}.amazonaws.com/"

    def upload_file(self, file_name, bucket_name, folder_name):
        # print(folder_name, bucket_name, file_name,
        #       self.base_url, settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        self.s3_conn.upload_file(
            file_name, bucket_name, f"{folder_name}/{file_name}")
        # print(resp)

    def get_file_link(self, file_name, folder_name):
        file_name = file_name.replace(" ", "T")#.replace(":", "%3A")
        file_link = self.base_url + folder_name + "/" + file_name
        # print("$$$$$$$$$$$$$$$$$$ ", file_name)
        return file_link
