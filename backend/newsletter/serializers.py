from rest_framework.serializers import ModelSerializer
from newsletter.models import Newsletter


class NewsletterEntrySerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        exclude = ("id",)


class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ("email",)

    def create(self, validated_data):
        instance, created = Newsletter.objects.get_or_create(**validated_data)
        if not created:
            instance.active = True
            instance.save()

        return instance
