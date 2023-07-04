from rest_framework import viewsets
from route.models.route_town_stoppage import RouteTownStoppage
from route.serializers.route_town_stoppage import RouteTownStoppageSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class CreateRouteTownStoppageView(viewsets.ModelViewSet):

    queryset = RouteTownStoppage.objects.all()
    serializer_class = RouteTownStoppageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
