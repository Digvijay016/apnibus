import json
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from bus.models.town_search import TownSearch
from bus.serializers.town_search import TownSearchSerializer


class CreateTownSearchView(viewsets.ModelViewSet):
    """
    working: Used for adding a bus.
    """

    # serializer_class = BusSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = TownSearch.objects.all()
    serializer_class = TownSearchSerializer

    http_method_names = ['get', 'post', 'put', 'delete']
