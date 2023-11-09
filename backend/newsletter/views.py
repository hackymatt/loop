from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from newsletter.serializers import NewsletterEntrySerializer, NewsletterSerializer
from newsletter.models import Newsletter
from profile.models import Profile


class NewsletterEntriesViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterEntrySerializer
    filterset_fields = "__all__"

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Brak dostępu."},
            )

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        if not profile.user_type == "A":
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"course": "Brak dostępu."},
            )

        return super().retrieve(request, *args, **kwargs)


class NewsletterSubscribeViewSet(ModelViewSet):
    http_method_names = ["post"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class NewsletterUnsubscribeViewSet(ModelViewSet):
    http_method_names = ["put"]

    @api_view(["PUT"])
    def unsubscribe(request, uuid):
        instance = Newsletter.objects.get(uuid=uuid)
        instance.active = False
        instance.save()

        return Response(
            status=status.HTTP_200_OK,
            data=NewsletterSerializer(instance).data,
        )
