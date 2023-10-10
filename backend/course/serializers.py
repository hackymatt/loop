from rest_framework.serializers import ModelSerializer
from course.models import Lesson, Course

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"



class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, source="lesson_set")

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "technology",
            "level",
            "price",
            "github_repo_link",
            "lessons",
        )


    def create_lessons(self, course, lessons):
        Lesson.objects.bulk_create([Lesson(course=course, title=lesson["title"], description=lesson["description"],
                                           duration=lesson["duration"], github_branch_link=lesson["github_branch_link"],price=lesson["price"])
                                           for lesson in lessons])
        
    def delete_lessons(self, course):
        Lesson.objects.filter(course=course).all().delete()

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")

        course = Course.objects.create(**validated_data)
        self.create_lessons(course=course, lessons=lessons) 

        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons")

        self.delete_lessons(course=instance)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.technology = validated_data.get("technology", instance.technology)
        instance.level = validated_data.get("level", instance.level)
        instance.price = validated_data.get("price", instance.price)
        instance.github_repo_link = validated_data.get("github_repo_link", instance.github_repo_link)
        instance.save()

        self.create_lessons(course=instance, lessons=lessons) 

        return instance
