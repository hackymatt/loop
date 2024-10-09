from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateTimeField,
)
from drf_extra_fields.fields import Base64ImageField
from post.models import Post, PostCategory
from profile.models import LecturerProfile, StudentProfile
from notification.utils import notify
from urllib.parse import quote_plus
from math import ceil


def notify_students(post):
    for student in StudentProfile.objects.all():
        path = quote_plus(f"{post.title.lower()}-{post.id}")
        notify(
            profile=student.profile,
            title="Dodano nowy artykuł",
            subtitle=post.title,
            description="Właśnie dodaliśmy nowy artykuł. Sprawdź go już teraz.",
            path=f"/posts/{path}",
            icon="mdi:blog",
        )

def get_lecturer_full_name(lecturer):
    return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name

def get_post_duration(post):
    words = post.content.split()
    return ceil(len(words) / 250)

class CategorySerializer(ModelSerializer):

    class Meta:
        model = PostCategory
        fields = (
            "id",
            "name",
        )

class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return get_lecturer_full_name(lecturer=lecturer)


class LecturerDetailsSerializer(ModelSerializer):
    full_name = SerializerMethodField("get_full_name")
    gender = CharField(source="profile.get_gender_display")
    image = Base64ImageField(source="profile.image", required=True)
    date_joined = DateTimeField(source="profile.user.date_joined")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "title",
            "description",
            "date_joined",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer):
        return get_lecturer_full_name(lecturer=lecturer)


class PostListSerializer(ModelSerializer):
    category = CategorySerializer()
    authors = LecturerSerializer(many=True)
    image = Base64ImageField(required=True)
    duration = SerializerMethodField("get_duration")

    class Meta:
        model = Post
        exclude = (
            "content",
            "visits",
            "modified_at",
        )

    def get_duration(self, post):
        return get_post_duration(post=post)


class PostGetSerializer(ModelSerializer):
    category = CategorySerializer()
    authors = LecturerDetailsSerializer(many=True)
    image = Base64ImageField(required=True)
    duration = SerializerMethodField("get_duration")

    class Meta:
        model = Post
        exclude = (
            "visits",
            "modified_at",
        )

    def get_duration(self, post):
        return get_post_duration(post=post)


class PostSerializer(ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Post
        fields = "__all__"

    def add_authors(self, post, authors):
        for author in authors:
            post.authors.add(author)

        return post

    def create(self, validated_data):
        authors = validated_data.pop("authors")

        post = Post.objects.create(**validated_data)
        post = self.add_authors(post=post, modules=authors)
        post.save()

        if post.active:
            notify_students(post=post)

        return post

    def update(self, instance, validated_data):
        authors = validated_data.pop("authors")

        instance.active = validated_data.get("active", instance.active)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.content = validated_data.get("content", instance.content)

        instance.image = validated_data.get("image", instance.image)

        instance.authors.clear()
        instance = self.add_authors(post=instance, authors=authors)

        instance.save()

        if instance.active:
            notify_students(post=instance)

        return instance
