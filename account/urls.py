from django.urls import include, path
from rest_framework.routers import DefaultRouter
from account.views.operator import CreateOperatorView

# from django.urls import path, include
# from account.views.aws_s3 import UploadAssetsToS3View
# from account.views.sales_team import UserAuthOTPViewset
# from operator_bd.urls import router
# from django.conf import settings
# from django.conf.urls.static import static
# from account.views.operator import CreateOperatorView, OperatorListView, OperatorUpdateView, OperatorRetrieveView, OperatorSearchView, OperatorUserAuthOTPViewset


# router.register("commuter/otp", CommuterOTPViewset)
# router.register("commuter/profile", CommuterProfileViewset)
# router.register("conductor/otp", BusDriverOTPViewset)
# router.register("sales-app/otp", UserAuthOTPViewset)

# urlpatterns = [
# path('/', CreateOperatorView.as_view(), name='create_operator_view')
# path('create', CreateOperatorView.as_view(), name='create_operator_view'),
# path('list', OperatorListView.as_view(), name='operator_list'),
# path('update/<str:id>', OperatorUpdateView.as_view(), name='operator_update'),
# path('retrieve/<str:id>', OperatorRetrieveView.as_view(),
#      name='operator_retrieve'),
# path('search', OperatorSearchView.as_view(), name='operator_search'),
# path('upload/assets', UploadAssetsToS3View.as_view(), name="upload_assets"),
# path('', include(router.urls)),
# ]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += router.urls
