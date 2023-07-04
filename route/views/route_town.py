from route.serializers.route_town import RouteTownSerializer
from route.models.route_town import RouteTown
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets


class CreateRouteTownView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = RouteTown.objects.all()
    serializer_class = RouteTownSerializer
