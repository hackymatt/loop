from rest_framework.serializers import ModelSerializer, IntegerField
from technology.models import Technology


class TechnologyListSerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "modified_at",
            "description",
        )


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = ("modified_at",)


class BestTechnologySerializer(ModelSerializer):
    courses_count = IntegerField()

    class Meta:
        model = Technology
        exclude = (
            "description",
            "modified_at",
            "created_at",
        )
