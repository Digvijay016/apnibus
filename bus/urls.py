from django.urls import path
from bus.models.bus_route_return import BusRouteReturn

# from account.views.operator import CreateOperatorView
# from bus.views.bus_via_route_pricing import AutoFillBusViaRoutePricing
from bus.views.bus import BusListView, CreateBusView
from bus.views.bus_route import BusRouteListView, CreateBusRouteView
from bus.views.bus_route_return import BusRouteListReturnView, CreateBusRouteReturnView
from bus.views.bus_route_town import BusRouteTownListView, CreateBusRouteTownView, UpdateBusRouteTownView
from bus.views.bus_route_town_stoppage import BusRouteTownStoppageListView, BusUpdateRouteTownStoppageView, CreateBusRouteTownStoppageView
# CreateBusRouteView, BusRouteListView,
# \
# CreateBusRouteTownView, BusRouteTownListView, CreateBusRouteTownStoppageView, BusRouteTownStoppageListView, \
# BusUpdateView, BusRetrieveView, CreateBusViaRouteView, BusViaRoutePricingListView, UpdateBusViaRoutePricingView, \
# UpdateBusRouteTownView, BusViaRouteListView, BusUpdateRouteTownStoppageView, BusRouteTownMappingView, BusSearchView, \
# UpdateBusRouteView, BusViaRouteUpdateView, BusRouteSearchView, BusDetailView, ExtendBusRouteJourneys, \
# AppVersionView, \
# AddUserDeviceView, LiveBusAddaTimeView, DeleteBusRouteView, BusRouteJourneyListView, BusRouteJourneyUpdateView, \
# DeleteBusView, ConductorViaRoutePricingListView, OperatorBusListView, OperatorCurrentTripDetailView, \
# OperatorAllTripDetailsView, OperatorProfileView, CommuterPricingExportView, CommuterPricingUpdateView, \
# BusRouteSearchAdminView, DeleteWrongJourneys, ExportBusViaRoutePricing, UploadCommuterBusViaRoutePricing, \
# UploadConductorBusViaRoutePricing, BusRouteSearchViewV2, OperatorBusListViewV2, \
# OperatorBusRouteJourneyTripHisabView, OperatorTicketDetailView, OperatorOnlineBookingView, \
# OperatorBusesActivityView, OperatorBusListDataView, BusActivityView, BusCommissionListView, BusCommissionUpdateView, \
# BusActivityViewV2, BusRouteSearchViewV3, BusRouteSearchViewV4

urlpatterns = [
    path('create', CreateBusView.as_view(), name='create_bus_view'),
    path('list', BusListView.as_view(), name='bus_list_view'),
    path('bus_route_create', CreateBusRouteView.as_view(),
         name='bus_route_create_view'),
    path('bus_route_list', BusRouteListView.as_view(),
         name='bus_route_list_view'),
    path('bus_route_town_create', CreateBusRouteTownView.as_view(),
         name='bus_route_town_create'),
    path('bus_route_town_list', BusRouteTownListView.as_view(),
         name='bus_route_town_list'),
    path('bus_route_town_update/<str:id>',
         UpdateBusRouteTownView.as_view(), name='bus_route_town_update'),
    path('bus_route_town_stoppage_create/', CreateBusRouteTownStoppageView.as_view(),
         name='bus_route_town_stoppage_create'),
    path('bus_route_town_stoppage_update/<str:id>', BusUpdateRouteTownStoppageView.as_view(),
         name='bus_route_town_stoppage_update'),
    path('bus_route_town_stoppage_list', BusRouteTownStoppageListView.as_view(),
         name='bus_route_town_stoppage_list'),
    path('bus_route_return_create', CreateBusRouteReturnView.as_view(),
         name='bus_route_return_create'),
    path('bus_route_return_list', BusRouteListReturnView.as_view(),
         name='bus_route_return_list'),
]
