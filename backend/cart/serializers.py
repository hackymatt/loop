from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
)
from course.models import Course, Lesson, Technology
from cart.models import Cart
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


class CartGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Cart
        exclude = ("student",)


class CartSerializer(ModelSerializer):
    course = IntegerField(required=False)
    lesson = IntegerField(required=False)

    class Meta:
        model = Cart
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
            cart_items = Cart.objects.filter(
                student=student, lesson__in=course_lessons
            ).all()

            if course_lessons.count() == cart_items.count():
                # delete whole course
                cart_items.delete()
            else:
                # add missing lessons
                for course_lesson in course_lessons:
                    Cart.objects.get_or_create(student=student, lesson=course_lesson)

        else:
            # manage specific lesson
            lesson = Lesson.objects.get(pk=lesson_id)
            cart_item = Cart.objects.filter(student=student, lesson=lesson).all()

            if cart_item.exists():
                # delete lesson
                cart_item.delete()
            else:
                # add lesson
                Cart.objects.create(student=student, lesson=lesson)

        return Cart.objects.filter(student=student).all()
