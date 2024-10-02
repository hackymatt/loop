from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
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
from config_global import FRONTEND_URL


class NewsletterEntriesViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterEntrySerializer
    filterset_class = NewsletterFilter
    permission_classes = [IsAuthenticated, IsAdminUser]


class NewsletterSubscribeViewSet(ModelViewSet):
    http_method_names = ["post"]

    @csrf_exempt
    def subscribe(request):
        send_email = False
        data = json.loads(request.body)
        instance, created = Newsletter.objects.get_or_create(**data)
        if not created:
            send_email = not instance.active
            instance.active = True
            instance.save()

        if send_email or created:
            mailer = Mailer()
            data = {
                **{
                    "unsubscribe_url": f"{FRONTEND_URL}/newsletter-unsubscribe/"
                    + str(instance.uuid),
                }
            }
            if created:
                coupons = Coupon.objects.filter(code="programista20")
                if coupons.exists():
                    coupon = coupons.first()
                else:
                    coupon = Coupon.objects.create(
                        code="programista20",
                        discount=20,
                        is_percentage=True,
                        all_users=True,
                        is_infinite=True,
                        uses_per_user=1,
                        active=True,
                        expiration_date=make_aware(
                            datetime.now() + timedelta(weeks=52 * 99)
                        ),
                    )
                data = {**data, **{"discount": coupon.code}}
            mailer.send(
                email_template="subscribe.html",
                to=[instance.email],
                subject="Potwierdzenie rejestracji w newsletterze",
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
