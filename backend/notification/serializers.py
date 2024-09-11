from rest_framework.serializers import ModelSerializer, CharField
from notification.models import Notification


class NotificationSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Notification
        exclude = ("profile",)
