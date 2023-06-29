from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from route.models.town import Town
from route.serializers.town import TownSerializer


class CreateTownView(viewsets.ModelViewSet):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
