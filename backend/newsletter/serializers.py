from rest_framework.serializers import ModelSerializer
from newsletter.models import Newsletter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class NewsletterEmail:
    def send(self, instance: Newsletter, email_template: str, mail_subject: str):
        data = {
            **{
                "unsubscribe_url": "http://localhost:8002/e-learning/newsletter-unsubscribe/"
                + str(instance.uuid),
            }
        }
        message = render_to_string(email_template, data)
        email = EmailMultiAlternatives(
            mail_subject, message, "from_email", to=[instance.email]
        )
        email.attach_alternative(message, "text/html")

        return email.send()


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

        email = NewsletterEmail()
        email.send(
            instance,
            "subscribe.html",
            "Potwierdzenie rejestracji w newsletterze.",
        )

        return instance
