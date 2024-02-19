from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from utils.permissions.permissions import IsStudent
from technology.serializers import TechnologySerializer, BestTechnologySerializer
from technology.filters import TechnologyFilter
from technology.models import Technology


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [AllowAny]
    filterset_class = TechnologyFilter

    def get_permissions(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "destroy"
        ):
            permission_classes = [IsAuthenticated & IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class BestTechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.all()
    serializer_class = BestTechnologySerializer
    filterset_class = TechnologyFilter
