from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from newsletter.serializers import NewsletterEntrySerializer, NewsletterSerializer
from newsletter.models import Newsletter
from newsletter.filters import NewsletterFilter
from coupon.models import Coupon
from django.views.decorators.csrf import csrf_exempt
from mailer.mailer import Mailer
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from config_global import FRONTEND_URL, DEFAULT_COUPON


class NewsletterEntriesViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterEntrySerializer
    filterset_class = NewsletterFilter
    permission_classes = [IsAuthenticated, IsAdminUser]


class NewsletterSubscribeAPIView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        data = request.data
        instance, created = Newsletter.objects.get_or_create(**data)

        send_email = created or not instance.active
        if not created:
            instance.active = True
            instance.save()

        if send_email:
            self._send_confirmation_email(instance, created)

        return Response(
            data=NewsletterSerializer(instance).data, status=status.HTTP_200_OK
        )

    def _send_confirmation_email(self, instance, created):
        mailer = Mailer()
        data = {
            "unsubscribe_url": f"{FRONTEND_URL}/newsletter-unsubscribe/{instance.uuid}",
            "discount": None,
        }

        if created:
            data["discount"] = DEFAULT_COUPON["code"]

        mailer.send(
            email_template="subscribe.html",
            to=[instance.email],
            subject="Potwierdzenie rejestracji w newsletterze",
            data=data,
        )


class NewsletterUnsubscribeAPIView(APIView):
    http_method_names = ["put"]

    def put(self, request, uuid):
        instance = Newsletter.objects.get(uuid=uuid)
        instance.active = False
        instance.save()

        return Response(NewsletterSerializer(instance).data, status=status.HTTP_200_OK)
