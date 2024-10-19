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
)
from profile.models import LecturerProfile


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / posts / <filename>
    return f"posts/{filename}"  # pragma: no cover


class PostCategory(BaseModel):
    name = CharField()

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


class Post(BaseModel):
    title = CharField()
    description = TextField()
    content = TextField()
    category = ForeignKey(PostCategory, on_delete=PROTECT, related_name="post_category")
    authors = ManyToManyField(LecturerProfile, related_name="post_authors")
    image = ImageField(upload_to=post_directory_path)
    visits = IntegerField(default=0)
    active = BooleanField(default=False)

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
