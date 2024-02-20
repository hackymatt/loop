from backend.base_model import BaseModel
from django.db.models import (
    TextField,
    Index,
)


class Skill(BaseModel):
    name = TextField()

    class Meta:
        db_table = "skill"
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
