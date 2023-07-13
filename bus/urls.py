# from django.urls import path
# from bus.models.bus_route_return import BusRouteReturn

# from bus.views.bus import BusListView, CreateBusView
# from bus.views.bus_route import BusRouteListView, CreateBusRouteView
# from bus.views.bus_route_return import BusRouteListReturnView, CreateBusRouteReturnView
# from bus.views.bus_route_town import BusRouteTownListView, CreateBusRouteTownView, UpdateBusRouteTownView
# from bus.views.bus_route_town_stoppage import BusRouteTownStoppageListView, BusUpdateRouteTownStoppageView, CreateBusRouteTownStoppageView

# urlpatterns = [
#     path('create', CreateBusView.as_view(), name='create_bus_view'),
#     path('list', BusListView.as_view(), name='bus_list_view'),
#     path('bus_route_create', CreateBusRouteView.as_view(),
#          name='bus_route_create_view'),
#     path('bus_route_list', BusRouteListView.as_view(),
#          name='bus_route_list_view'),
#     path('bus_route_town_create', CreateBusRouteTownView.as_view(),
#          name='bus_route_town_create'),
#     path('bus_route_town_list', BusRouteTownListView.as_view(),
#          name='bus_route_town_list'),
#     path('bus_route_town_update/<str:id>',
#          UpdateBusRouteTownView.as_view(), name='bus_route_town_update'),
#     path('bus_route_town_stoppage_create/', CreateBusRouteTownStoppageView.as_view(),
#          name='bus_route_town_stoppage_create'),
#     path('bus_route_town_stoppage_update/<str:id>', BusUpdateRouteTownStoppageView.as_view(),
#          name='bus_route_town_stoppage_update'),
#     path('bus_route_town_stoppage_list', BusRouteTownStoppageListView.as_view(),
#          name='bus_route_town_stoppage_list'),
#     path('bus_route_return_create', CreateBusRouteReturnView.as_view(),
#          name='bus_route_return_create'),
#     path('bus_route_return_list', BusRouteListReturnView.as_view(),
#          name='bus_route_return_list'),
# ]
