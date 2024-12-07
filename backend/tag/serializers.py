from rest_framework.serializers import ModelSerializer
from tag.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = ("modified_at",)
