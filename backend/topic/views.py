from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from topic.serializers import TopicSerializer
from topic.filters import TopicFilter
from topic.models import Topic


class TopicViewSet(ModelViewSet):
    """ViewSet for managing topics."""

    queryset = Topic.objects.all().order_by("id")
    serializer_class = TopicSerializer
    permission_classes = [AllowAny]
    filterset_class = TopicFilter
    http_method_names = ["get", "post", "put", "delete"]

    def get_permissions(self):
        """Return the list of permissions that the user must satisfy to access this view."""
        if self.action in ["create", "update", "destroy"]:
            return [permission() for permission in [IsAuthenticated, IsAdminUser]]
        return super().get_permissions()  # Default permission for read actions
