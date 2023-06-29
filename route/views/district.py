
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from route.models.district import District
from route.serializers.district import DistrictSerializer


class CreateDistrictView(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
