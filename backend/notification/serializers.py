from rest_framework.serializers import ModelSerializer, CharField
from notification.models import Notification


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        exclude = ("profile",)
