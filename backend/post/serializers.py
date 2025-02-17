from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    DateTimeField,
)
from drf_extra_fields.fields import Base64ImageField
from post.models import Post, PostCategory
from tag.models import Tag
from profile.models import LecturerProfile
from django.db.models import Case, When, IntegerField


class CategorySerializer(ModelSerializer):
    class Meta:
        model = PostCategory
        fields = (
            "id",
            "name",
        )


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        exclude = (
            "modified_at",
            "created_at",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.gender")
    image = Base64ImageField(source="profile.image", required=True)

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class LecturerDetailsSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.gender")
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

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


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
    duration = SerializerMethodField()

    class Meta:
        model = Post
        exclude = (
            "content",
            "tags",
            "visits",
            "modified_at",
            "created_at",
        )

    def get_duration(self, post: Post):
        return post.duration


class PostGetSerializer(ModelSerializer):
    category = CategorySerializer()
    tags = SerializerMethodField()
    authors = LecturerDetailsSerializer(many=True)
    image = Base64ImageField(required=True)
    duration = SerializerMethodField()
    previous_post = SerializerMethodField()
    next_post = SerializerMethodField()

    class Meta:
        model = Post
        exclude = (
            "visits",
            "modified_at",
            "created_at",
        )

    def get_duration(self, post: Post):
        return post.duration

    def get_previous_post(self, post: Post):
        if not post.previous_post:
            return None
        post = Post.objects.get(id=post.previous_post)
        return PostNavigationSerializer(
            post, context={"request": self.context.get("request")}
        ).data

    def get_next_post(self, post: Post):
        if not post.next_post:
            return None
        post = Post.objects.get(id=post.next_post)
        return PostNavigationSerializer(
            post, context={"request": self.context.get("request")}
        ).data

    def get_tags(self, post: Post):
        tag_ids = list(
            Post.tags.through.objects.filter(post=post)
            .order_by("id")
            .values_list("tag_id", flat=True)
        )
        preserved_order = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(tag_ids)],
            output_field=IntegerField(),
        )
        tags = Tag.objects.filter(id__in=tag_ids).order_by(preserved_order)
        return TagSerializer(tags, many=True).data


class PostSerializer(ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Post
        fields = "__all__"

    def add_authors(self, post: Post, authors):
        for author in authors:
            post.authors.add(author)

        return post

    def add_tags(self, post: Post, tags):
        names = [tag.name for tag in tags]
        existing_names = set(
            Tag.objects.filter(name__in=names).values_list("name", flat=True)
        )

        missing_tags = [Tag(name=name) for name in set(names) - existing_names]

        Tag.objects.bulk_create(missing_tags, ignore_conflicts=True)

        tags_objs = Tag.objects.filter(name__in=names)

        for tags_obj in tags_objs:
            post.tags.add(tags_obj)

        return post

    def create(self, validated_data):
        authors = validated_data.pop("authors")
        tags = validated_data.pop("tags")

        post = Post.objects.create(**validated_data)
        post = self.add_authors(post=post, authors=authors)
        post = self.add_tags(post=post, tags=tags)
        post.save()

        return post

    def update(self, instance: Post, validated_data):
        authors = validated_data.pop("authors")
        tags = validated_data.pop("tags")

        instance.active = validated_data.get("active", instance.active)
        instance.publication_date = validated_data.get(
            "publication_date", instance.publication_date
        )
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.content = validated_data.get("content", instance.content)

        instance.image = validated_data.get("image", instance.image)

        instance.authors.clear()
        instance = self.add_authors(post=instance, authors=authors)
        instance.tags.clear()
        instance = self.add_tags(post=instance, tags=tags)

        instance.save()

        return instance


class PostCategorySerializer(ModelSerializer):
    class Meta:
        model = PostCategory
        exclude = ("modified_at",)
