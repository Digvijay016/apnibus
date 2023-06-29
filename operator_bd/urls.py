"""Operators BD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import Route, DynamicRoute, SimpleRouter
from rest_framework.routers import DefaultRouter
# from django.conf import settings
# from django.conf.urls.static import static

from account.views.operator import CreateOperatorView
from bus.views.bus import CreateBusView
from bus.views.bus_route import CreateBusRouteView
from bus.views.bus_route_town import CreateBusRouteTownView
from pricing.views.price import CreatePriceView
from route.views.district import CreateDistrictView
from route.views.route import CreateRouteView
from route.views.route_town import CreateRouteTownView
from route.views.route_town_stoppage import CreateRouteTownStoppageView
from route.views.state import CreateStateView
from route.views.town import CreateTownView
from route.views.town_stoppage import CreateTownStoppageView


class CustomRouter(SimpleRouter):
    """
    A router for read-only APIs, which use trailing slashes.
    """

    """
    Match URL path first
    """

    routes = [
        DynamicRoute(
            url=r"^{prefix}/{url_path}/$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
        Route(
            url=r"^{prefix}/{lookup}/$",
            mapping={"get": "retrieve", "put": "update",
                     "patch": "partial_update", "delete": "destroy"},
            name="{basename}-retrieve-update",
            detail=True,
            initkwargs={"suffix": "Retrieve/Update"},
        ),
        Route(
            url=r"^{prefix}/$",
            mapping={"get": "list", "post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}/$",
            name="{basename}-{url_name}",
            detail=True,
            initkwargs={},
        ),
    ]


router = DefaultRouter()
router.register(r'operators', CreateOperatorView)
router.register(r'bus', CreateBusView)
router.register(r'bus_route', CreateBusRouteView)
router.register(r'bus_route_town', CreateBusRouteTownView)
router.register(r'pricing', CreatePriceView)
router.register(r'towns', CreateTownView)
router.register(r'district', CreateDistrictView)
router.register(r'states', CreateStateView)
router.register(r'town_stoppage', CreateTownStoppageView)
router.register(r'route', CreateRouteView)
router.register(r'route_town', CreateRouteTownView)
router.register(r'route_town_stoppage', CreateRouteTownStoppageView)
# router.register(r'routes', CreateRouteView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('bus/', include('bus.urls')),
    # path('pricing/', include('pricing.urls')),
    # path('route/', include('route.urls'))
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
