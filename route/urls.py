from django.urls import path, include
from account.views.aws_s3 import UploadAssetsToS3View
from account.views.sales_team import UserAuthOTPViewset
from account.urls import router

router.register("sales-app/otp", UserAuthOTPViewset)

urlpatterns = [
]

urlpatterns += router.urls
