from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from tag.serializers import TagSerializer
from tag.filters import TagFilter
from tag.models import Tag


class TagViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Tag.objects.add_post_count().add_course_count().all().order_by("id")
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filterset_class = TagFilter

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
