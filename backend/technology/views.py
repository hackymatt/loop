from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from technology.serializers import TechnologySerializer, BestTechnologySerializer
from technology.filters import TechnologyFilter
from technology.models import Technology


class TechnologyViewSet(ModelViewSet):
    queryset = Technology.objects.all().order_by("id")
    serializer_class = TechnologySerializer
    permission_classes = [AllowAny]
    filterset_class = TechnologyFilter
    http_method_names = ["get", "post", "put", "delete"]

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class BestTechnologyViewSet(ModelViewSet):
    queryset = Technology.objects.all().order_by("id")
    serializer_class = BestTechnologySerializer
    filterset_class = TechnologyFilter
    http_method_names = ["get"]
