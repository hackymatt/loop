from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
)
from course.models import Course
from lesson.models import Lesson, Technology
from wishlist.models import Wishlist
from profile.models import Profile


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    technology = TechnologySerializer()

    class Meta:
        model = Course
        exclude = ("active", "skills", "topics")


class LessonSerializer(ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"


class WishlistGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Wishlist
        exclude = ("student",)


class WishlistSerializer(ModelSerializer):
    course = IntegerField(required=False)
    lesson = IntegerField(required=False)

    class Meta:
        model = Wishlist
        fields = (
            "student",
            "course",
            "lesson",
        )

    def create(self, validated_data):
        student_id = validated_data.pop("student")
        student = Profile.objects.get(pk=student_id)

        course_id = validated_data.get("course", None)
        lesson_id = validated_data.get("lesson", None)

        if course_id:
            # manage whole course
            course = Course.objects.get(pk=course_id)
            course_lessons = course.lessons.all()
            wishlist_items = Wishlist.objects.filter(
                student=student, lesson__in=course_lessons
            ).all()

            if course_lessons.count() == wishlist_items.count():
                # delete whole course
                wishlist_items.delete()
            else:
                # add missing lessons
                for course_lesson in course_lessons:
                    Wishlist.objects.get_or_create(
                        student=student, lesson=course_lesson
                    )

        else:
            # manage specific lesson
            lesson = Lesson.objects.get(pk=lesson_id)
            wishlist_item = Wishlist.objects.filter(
                student=student, lesson=lesson
            ).all()

            if wishlist_item.exists():
                # delete lesson
                wishlist_item.delete()
            else:
                # add lesson
                Wishlist.objects.create(student=student, lesson=lesson)

        return Wishlist.objects.filter(student=student).all()
