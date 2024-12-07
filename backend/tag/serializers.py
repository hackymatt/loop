from rest_framework.serializers import ModelSerializer, SerializerMethodField
from tag.models import Tag


class TagSerializer(ModelSerializer):
    post_count = SerializerMethodField()
    course_count = SerializerMethodField()

    class Meta:
        model = Tag
        exclude = ("modified_at",)

    def get_post_count(self, tag: Tag):
        return tag.post_count

    def get_course_count(self, tag: Tag):
        return tag.course_count


class TagCreateSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = ("modified_at",)
