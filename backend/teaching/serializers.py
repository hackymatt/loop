from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
)
from course.models import Course
from lesson.models import Lesson, Technology
from teaching.models import Teaching
from profile.models import Profile


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class TeachingGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Teaching
        exclude = ("lecturer",)


class TeachingSerializer(ModelSerializer):
    course = IntegerField(required=False)
    lesson = IntegerField(required=False)

    class Meta:
        model = Teaching
        fields = (
            "lecturer",
            "course",
            "lesson",
        )

    def create(self, validated_data):
        lecturer_id = validated_data.pop("lecturer")
        lecturer = Profile.objects.get(pk=lecturer_id)

        course_id = validated_data.get("course", None)
        lesson_id = validated_data.get("lesson", None)

        if course_id:
            # manage whole course
            course = Course.objects.get(pk=course_id)
            course_lessons = course.lessons.all()
            teaching_items = Teaching.objects.filter(
                lecturer=lecturer, lesson__in=course_lessons
            ).all()

            if course_lessons.count() == teaching_items.count():
                # delete whole course
                teaching_items.delete()
            else:
                # add missing lessons
                for course_lesson in course_lessons:
                    Teaching.objects.get_or_create(
                        lecturer=lecturer, lesson=course_lesson
                    )

        else:
            # manage specific lesson
            lesson = Lesson.objects.get(pk=lesson_id)
            teaching_item = Teaching.objects.filter(
                lecturer=lecturer, lesson=lesson
            ).all()

            if teaching_item.exists():
                # delete lesson
                teaching_item.delete()
            else:
                # add lesson
                Teaching.objects.create(lecturer=lecturer, lesson=lesson)

        return Teaching.objects.filter(lecturer=lecturer).all()
