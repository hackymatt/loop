from rest_framework.serializers import ModelSerializer
from review.models import Review
from profile.models import Profile


class BestReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = (
            "lesson",
            "rating",
        )


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = ("profile",)

    def create(self, validated_data):
        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        return Review.objects.create(**validated_data, profile=profile)
