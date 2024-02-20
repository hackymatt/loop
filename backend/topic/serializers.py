from rest_framework.serializers import ModelSerializer
from topic.models import Topic


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        exclude = ("modified_at",)
