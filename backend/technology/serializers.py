from rest_framework.serializers import ModelSerializer, IntegerField
from technology.models import Technology


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("modified_at",)


class BestTechnologySerializer(ModelSerializer):
    courses_count = IntegerField()

    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "created_at",
        )
