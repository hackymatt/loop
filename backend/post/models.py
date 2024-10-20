from core.base_model import BaseModel
from django.db.models import (
    ManyToManyField,
    ForeignKey,
    CharField,
    TextField,
    IntegerField,
    BooleanField,
    ImageField,
    Index,
    PROTECT,
    QuerySet,
    Manager,
    Value,
    FloatField,
    OuterRef,
    Subquery,
    Count,
)
from profile.models import LecturerProfile
from config_global import WORDS_PER_MINUTE
from django.db.models.functions import Length, Ceil, Cast, Coalesce


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / posts / <filename>
    return f"posts/{filename}"  # pragma: no cover


class PostCategoryQuerySet(QuerySet):
    def add_post_count(self):
        return self.annotate(posts_count=Count("post_category"))


class PostCategoryManager(Manager):
    def get_queryset(self):
        return PostCategoryQuerySet(self.model, using=self._db)

    def add_post_count(self):
        return self.get_queryset().add_post_count()


class PostCategory(BaseModel):
    name = CharField()

    objects = PostCategoryManager()

    class Meta:
        db_table = "post_category"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]


class PostQuerySet(QuerySet):
    def add_duration(self):
        return self.annotate(
            duration=Ceil(
                Cast(Length("content"), FloatField()) / Value(WORDS_PER_MINUTE)
            )
        )

    def add_previous_post(self):
        previous_post = Post.objects.filter(
            created_at__lt=OuterRef("created_at"), active=True
        ).values("id")[:1]

        return self.annotate(
            previous_post=Coalesce(
                Subquery(previous_post), Value(None, output_field=IntegerField())
            )
        )

    def add_next_post(self):
        next_post = Post.objects.filter(
            created_at__gt=OuterRef("created_at"), active=True
        ).values("id")[:1]

        return self.annotate(
            next_post=Coalesce(
                Subquery(next_post), Value(None, output_field=IntegerField())
            )
        )


class PostManager(Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def add_duration(self):
        return self.get_queryset().add_duration()

    def add_previous_post(self):
        return self.get_queryset().add_previous_post()

    def add_next_post(self):
        return self.get_queryset().add_next_post()


class Post(BaseModel):
    title = CharField()
    description = TextField()
    content = TextField()
    category = ForeignKey(PostCategory, on_delete=PROTECT, related_name="post_category")
    authors = ManyToManyField(LecturerProfile, related_name="post_authors")
    image = ImageField(upload_to=post_directory_path)
    visits = IntegerField(default=0)
    active = BooleanField(default=False)

    objects = PostManager()

    class Meta:
        db_table = "post"
        ordering = ["id"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
        ]
