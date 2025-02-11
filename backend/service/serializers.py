from rest_framework.serializers import ModelSerializer
from service.models import Service


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        exclude = (
            "created_at",
            "modified_at",
        )
