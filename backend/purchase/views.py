from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from purchase.serializers import PurchaseSerializer
from purchase.models import LessonPurchase


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPurchase.objects.all()
    serializer_class = PurchaseSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"purchase": "Użytkownik niezalogowany."},
            )

        return super().list(request, *args, **kwargs)
