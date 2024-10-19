from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import Case, When, IntegerField
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
        lesson_ids = list(
            module.lessons.through.objects.order_by("id").values_list(
                "lesson_id", flat=True
            )
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(lesson_ids)],
            output_field=IntegerField(),
        )
        lessons = Lesson.objects.filter(id__in=lesson_ids).order_by(preserved_order)
        return LessonSerializer(lessons, many=True).data


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
