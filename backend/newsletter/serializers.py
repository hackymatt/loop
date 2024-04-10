from rest_framework.serializers import ModelSerializer
from newsletter.models import Newsletter
from mailer.mailer import Mailer


class NewsletterEntrySerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        exclude = ("id",)


class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ("email",)
