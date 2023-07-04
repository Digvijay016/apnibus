from rest_framework import viewsets

from route.models.route_missing_town import RouteMissingTown
from route.serializers.route_missing_town import RouteMissingTownSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RouteMissingTownView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = RouteMissingTown.objects.all()
    serializer_class = RouteMissingTownSerializer
