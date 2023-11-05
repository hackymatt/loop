from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from newsletter.serializers import NewsletterEntrySerializer, NewsletterSerializer
from newsletter.models import Newsletter


class NewsletterEntriesViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterEntrySerializer

    def get_queryset(self):
        if self.action == "list":
            active = self.request.query_params.get("active", None)
            if active:
                return self.queryset.filter(active=active).all()
            else:
                return self.queryset

        return self.queryset


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
