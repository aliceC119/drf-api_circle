from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Group
from .serializers import GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'members__username']
    filterset_fields = ['name', 'members__username']
