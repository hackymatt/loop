from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from service.serializers import ServiceSerializer
from service.models import Service
from service.filters import ServiceFilter


class ServiceViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put"]
    queryset = Service.objects.all().order_by("id")
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filterset_class = ServiceFilter
