from backend.base_model import BaseModel
from django.db.models import (
    CharField,
    Index,
)


class Technology(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = "technology"
        ordering = ["id"]
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
