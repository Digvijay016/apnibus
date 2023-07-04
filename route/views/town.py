from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from route.models.town import Town
from route.serializers.town import TownSerializer
from django.db.models import F


class CreateTownView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.query_params.get('search', None)

        queryset = queryset.filter(status='active')

        if search_param:
            queryset = queryset.filter(name__icontains=search_param)
        
            queryset = queryset.annotate(district_name=F('district__name'))

        return queryset
