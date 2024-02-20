from rest_framework.serializers import ModelSerializer
from skill.models import Skill


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        exclude = ("modified_at",)
