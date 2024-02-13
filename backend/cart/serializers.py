from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    ListField,
)
from lesson.models import Lesson
from cart.models import Cart
from profile.models import Profile


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CartGetSerializer(ModelSerializer):
    lesson = LessonSerializer()

    class Meta:
        model = Cart
        exclude = ("student",)


class CartSerializer(ModelSerializer):
    lessons = ListField(child=IntegerField())

    class Meta:
        model = Cart
        fields = ("lessons",)

    def create(self, validated_data):
        user = self.context.get("request").user
        student = Profile.objects.get(user=user)

        lesson_ids = validated_data.get("lessons")

        for lesson_id in lesson_ids:
            lesson = Lesson.objects.get(pk=lesson_id)
            Cart.objects.get_or_create(lesson=lesson, student=student)

        return Cart.objects.filter(student=student).all()

    def destroy(self, validated_data):
        user = self.context.get("request").user
        student = Profile.objects.get(user=user)

        lesson_ids = validated_data.get("lessons")

        for lesson_id in lesson_ids:
            lesson = Lesson.objects.get(pk=lesson_id)
            Cart.objects.filter(lesson=lesson, student=student).delete()

        return Cart.objects.filter(student=student).all()
