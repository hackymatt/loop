from rest_framework.serializers import ModelSerializer, SerializerMethodField
from technology.models import Technology
from course.models import Course


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("modified_at",)


class BestTechnologySerializer(ModelSerializer):
    courses_count = SerializerMethodField()

    class Meta:
        model = Technology
        exclude = ("modified_at", "created_at")

    def get_courses_count(self, technology):
        return technology.courses_count
