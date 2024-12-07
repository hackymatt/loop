from core.base_model import BaseModel
from django.db.models import (
    TextField,
    Index,
)


class Tag(BaseModel):
    name = TextField()

    class Meta:
        db_table = "tags"
        ordering = ["name"]
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            ),
            Index(
                fields=[
                    "name",
                ]
            ),
        ]
