from django.urls import path
from pricing.views.price import CreatePriceView, DeletePricingView, PriceListView, PricingUpdateView

urlpatterns = [
    path('create', CreatePriceView.as_view(), name='create_price_view'),
    path('list', PriceListView.as_view(), name='price_list'),
    path('update/<str:bus_route>', PricingUpdateView.as_view(),
         name='price_update'),
    path('delete/', DeletePricingView.as_view(),
         name='price_delete')
    # path('update/<str:id>', OperatorUpdateView.as_view(), name='operator_update'),
    # path('retrieve/<str:id>', OperatorRetrieveView.as_view(),
    #      name='operator_retrieve'),
    # path('search', OperatorSearchView.as_view(), name='operator_search'),
    # path('', include(router.urls)),
]
