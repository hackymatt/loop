from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from notification.serializers import NotificationSerializer
from notification.models import Notification
from profile.models import Profile


class NotificationViewSet(ModelViewSet):
    http_method_names = ["get", "put"]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return self.queryset.filter(profile=profile)
