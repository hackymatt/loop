from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from newsletter.serializers import NewsletterEntrySerializer, NewsletterSerializer
from newsletter.models import Newsletter
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from mailer.mailer import Mailer
import json


class NewsletterEntriesViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterEntrySerializer
    filterset_fields = "__all__"
    permission_classes = [IsAuthenticated & IsAdminUser]


class NewsletterSubscribeViewSet(ModelViewSet):
    http_method_names = ["post"]

    @csrf_exempt
    def subscribe(request):
        data = json.loads(request.body)
        instance, created = Newsletter.objects.get_or_create(**data)
        if not created:
            instance.active = True
            instance.save()

        mailer = Mailer()
        data = {
            **{
                "unsubscribe_url": f"{settings.BASE_FRONTEND_UR}/newsletter-unsubscribe/"
                + str(instance.uuid),
            }
        }
        mailer.send(
            email_template="subscribe.html",
            to=[instance.email],
            subject="Potwierdzenie rejestracji w newsletterze.",
            data=data,
        )

        return JsonResponse(NewsletterSerializer(instance).data)


class NewsletterUnsubscribeViewSet(ModelViewSet):
    http_method_names = ["put"]

    @csrf_exempt
    def unsubscribe(request, uuid):
        instance = Newsletter.objects.get(uuid=uuid)
        instance.active = False
        instance.save()

        return JsonResponse(NewsletterSerializer(instance).data)
