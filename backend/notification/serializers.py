from rest_framework.serializers import ModelSerializer, CharField
from notification.models import Notification


class NotificationSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Notification
        exclude = ("profile",)

    def update(self, instance, validated_data):
        status = validated_data.pop("get_status_display", instance.status)

        Notification.objects.filter(pk=instance.pk).update(
            **validated_data, status=status
        )
        instance = Notification.objects.get(pk=instance.pk)

        return instance
