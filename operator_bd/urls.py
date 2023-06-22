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
            mapping={"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"},
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


router = CustomRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('operator/', include('account.urls')),
    path('bus/', include('bus.urls'))
]
