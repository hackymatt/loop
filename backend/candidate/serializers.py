from rest_framework.serializers import ModelSerializer
from candidate.models import Candidate


class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        exclude = ("modified_at",)
