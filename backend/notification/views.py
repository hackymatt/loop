from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from notification.serializers import NotificationSerializer
from notification.models import Notification
from notification.filters import NotificationFilter
from profile.models import Profile


class NotificationViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Notification.objects.all().order_by("id")
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = NotificationFilter

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return self.queryset.filter(profile=profile)
