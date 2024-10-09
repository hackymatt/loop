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


def get_lecturer_full_name(lecturer):
    return lecturer.profile.user.first_name + " " + lecturer.profile.user.last_name


def get_post_duration(post):
    words = post.content.split()
    return ceil(len(words) / 250)


def get_post_navigation(post, filter):
    lookup_field_name = f"created_at__{filter}"
    current_post_created_at = post.created_at
    posts = Post.objects.filter(
        **{lookup_field_name: current_post_created_at, "active": True}
    )
    if posts.exists():
        return PostNavigationSerializer(instance=posts.first()).data
    return None


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


class PostNavigationSerializer(ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "image",
        )


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
    previous_post = SerializerMethodField("get_previous_post")
    next_post = SerializerMethodField("get_next_post")

    class Meta:
        model = Post
        exclude = (
            "visits",
            "modified_at",
        )

    def get_duration(self, post):
        return get_post_duration(post=post)

    def get_previous_post(self, post):
        return get_post_navigation(post=post, filter="lt")

    def get_next_post(self, post):
        return get_post_navigation(post=post, filter="gt")


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
        post = self.add_authors(post=post, authors=authors)
        post.save()

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

        return instance


class PostCategorySerializer(ModelSerializer):
    class Meta:
        model = PostCategory
        exclude = ("modified_at",)
