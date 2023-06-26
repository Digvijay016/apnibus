from django.urls import path
from pricing.views.price import CreatePriceView, PriceListView

urlpatterns = [
    path('create', CreatePriceView.as_view(), name='create_operator_view'),
    path('list', PriceListView.as_view(), name='operator_list'),
    # path('update/<str:id>', OperatorUpdateView.as_view(), name='operator_update'),
    # path('retrieve/<str:id>', OperatorRetrieveView.as_view(),
    #      name='operator_retrieve'),
    # path('search', OperatorSearchView.as_view(), name='operator_search'),
    # path('', include(router.urls)),
]
