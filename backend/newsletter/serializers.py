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

    def create(self, validated_data):
        instance, created = Newsletter.objects.get_or_create(**validated_data)
        if not created:
            instance.active = True
            instance.save()

        mailer = Mailer()
        data = {
            **{
                "unsubscribe_url": "http://localhost:8002/e-learning/newsletter-unsubscribe/"
                + str(instance.uuid),
            }
        }
        mailer.send(
            email_template="subscribe.html",
            to=[instance.email],
            subject="Potwierdzenie rejestracji w newsletterze.",
            data=data,
        )

        return instance
