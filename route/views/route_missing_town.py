from rest_framework import viewsets

from route.models.route_missing_town import RouteMissingTown
from route.serializers.route_missing_town import RouteMissingTownSerializer


class RouteMissingTownView(viewsets.ModelViewSet):

    queryset = RouteMissingTown.objects.all()
    serializer_class = RouteMissingTownSerializer
