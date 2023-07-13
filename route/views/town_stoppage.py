from rest_framework import viewsets
from route.serializers.town_stoppage import TownStoppageSerializer
from route.models.town_stoppage import TownStoppage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateTownStoppageView(viewsets.ModelViewSet):
    """
    working: Using this API to create town stoppage
    """

    queryset = TownStoppage.objects.all()
    serializer_class = TownStoppageSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
