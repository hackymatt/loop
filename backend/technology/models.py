from backend.base_model import BaseModel
from django.db.models import (
    CharField,
    Index,
)


class Technology(BaseModel):
    name = CharField()

    class Meta:
        db_table = "technology"
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
