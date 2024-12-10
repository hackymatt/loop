from core.base_model import BaseModel
from django.db.models import (
    TextField,
    Index,
)


class Candidate(BaseModel):
    name = TextField()

    class Meta:
        db_table = "candidate"
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
