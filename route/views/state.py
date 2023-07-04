
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from route.models.state import State
from route.serializers.state import StateSerializer


class CreateStateView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = State.objects.all()
    serializer_class = StateSerializer
