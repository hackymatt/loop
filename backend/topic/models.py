from backend.base_model import BaseModel
from django.db.models import (
    TextField,
    Index,
)


class Topic(BaseModel):
    name = TextField()

    class Meta:
        db_table = "topic"
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
