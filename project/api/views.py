from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Schedule
from .serializers import ScheduleSerializer
from .permissions import IsSalesOrConstructionUser

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticatedReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'location', 'description']
    filterset_fields = ['schedule_date', 'location']
    ordering_fields = ['schedule_date', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSalesOrConstructionUser()]
        return super().get_permissions() 