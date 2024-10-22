from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from technology.serializers import TechnologySerializer, BestTechnologySerializer
from technology.filters import TechnologyFilter
from technology.models import Technology


class TechnologyViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Technology.objects.all().order_by("id")
    serializer_class = TechnologySerializer
    permission_classes = [AllowAny]
    filterset_class = TechnologyFilter

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        courses_count_from = self.request.query_params.get("courses_count_from", None)
        if courses_count_from:
            return self.queryset.add_courses_count()
        return self.queryset


class BestTechnologyViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Technology.objects.add_courses_count().all().order_by("id")
    serializer_class = BestTechnologySerializer
    filterset_class = TechnologyFilter
