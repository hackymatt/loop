from rest_framework.serializers import ModelSerializer, SerializerMethodField
from module.models import Module
from lesson.models import Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
        )


class ModuleGetSerializer(ModelSerializer):
    lessons = SerializerMethodField()

    class Meta:
        model = Module
        exclude = (
            "created_at",
            "modified_at",
        )

    def get_lessons(self, module: Module):
        return LessonSerializer(module.ordered_lessons, many=True).data


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        exclude = (
            "created_at",
            "modified_at",
        )

    def create(self, validated_data):
        lessons = validated_data.pop("lessons", [])

        module = Module.objects.create(**validated_data)
        if lessons:
            module.lessons.set(lessons)
        module.save()

        return module

    def update(self, instance: Module, validated_data):
        lessons = validated_data.pop("lessons", None)
        Module.objects.filter(pk=instance.pk).update(**validated_data)

        if lessons is not None:
            instance.lessons.clear()
            instance.lessons.set(lessons)

        return instance
