from django.urls import path
from operator_bd.urls import router
from account.views.operator import CreateOperatorView, OperatorListView, OperatorUpdateView, OperatorRetrieveView, OperatorSearchView

# router.register("commuter/otp", CommuterOTPViewset)
# router.register("commuter/profile", CommuterProfileViewset)
# router.register("conductor/otp", BusDriverOTPViewset)
# router.register("operator-app/otp", OperatorUserAuthOTPViewset)

urlpatterns = [
    path('create', CreateOperatorView.as_view(), name='create_operator_view'),
    path('list', OperatorListView.as_view(), name='operator_list'),
    path('update/<str:id>', OperatorUpdateView.as_view(), name='operator_update'),
    path('retrieve/<str:id>', OperatorRetrieveView.as_view(), name='operator_retrieve'),
    path('search', OperatorSearchView.as_view(), name='operator_search'),
]

# urlpatterns += router.urls
