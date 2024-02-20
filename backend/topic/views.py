from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from topic.serializers import TopicSerializer
from topic.filters import TopicFilter
from topic.models import Topic


class TopicViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
    filterset_class = TopicFilter

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
