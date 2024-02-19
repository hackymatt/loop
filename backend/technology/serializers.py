from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lesson.models import Lesson
from technology.models import Technology
from course.models import Course


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("modified_at",)


class BestTechnologySerializer(ModelSerializer):
    courses_count = SerializerMethodField("get_course_count")

    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )

    def get_course_count(self, technology):
        lessons = Lesson.technologies.through.objects.filter(
            technology_id=technology
        ).values("lesson_id")
        courses = (
            Course.lessons.through.objects.filter(lesson_id__in=lessons)
            .values("course_id")
            .distinct()
        )
        return courses.count()
