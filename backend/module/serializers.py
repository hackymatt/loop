from rest_framework.serializers import ModelSerializer, SerializerMethodField
from module.models import Module
from lesson.models import Lesson


def get_module_lessons(module):
    module_lessons = (
        Module.lessons.through.objects.filter(module=module).all().order_by("id")
    )
    return [
        Lesson.objects.get(id=module_lesson.lesson_id)
        for module_lesson in module_lessons
    ]


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

    def get_lessons(self, module):
        return LessonSerializer(get_module_lessons(module=module), many=True).data


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        exclude = (
            "created_at",
            "modified_at",
        )

    def add_lesson(self, module, lessons):
        for lesson in lessons:
            module.lessons.add(lesson)

        return module

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")

        module = Module.objects.create(**validated_data)
        module = self.add_lesson(module=module, lessons=lessons)
        module.save()

        return module

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons")

        Module.objects.filter(pk=instance.pk).update(**validated_data)

        instance = Module.objects.get(pk=instance.pk)
        instance.lessons.clear()
        instance = self.add_lesson(module=instance, lessons=lessons)
        instance.save()

        return instance
