from rest_framework.serializers import ModelSerializer, SerializerMethodField
from lesson.models import Lesson
from technology.models import Technology
from course.models import Course
from module.models import Module


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
        modules = Module.lessons.through.objects.filter(lesson_id__in=lessons).values(
            "module_id"
        )
        courses = (
            Course.modules.through.objects.filter(module_id__in=modules)
            .values("course_id")
            .distinct()
        )
        return courses.count()
