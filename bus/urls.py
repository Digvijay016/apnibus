from django.urls import path

# from account.views.operator import CreateOperatorView
# from bus.views.bus_via_route_pricing import AutoFillBusViaRoutePricing
from bus.views.bus import BusListView, CreateBusView
from bus.views.bus_route import BusRouteListView, CreateBusRouteView
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
    path('bus_route_list', BusRouteListView.as_view(), name='bus_route_list_view'),
]
