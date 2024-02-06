from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from purchase.serializers import PurchaseSerializer, PurchaseGetSerializer
from purchase.models import LessonPurchase
from purchase.filters import PurchaseFilter
from profile.models import Profile


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = LessonPurchase.objects.all()
    serializer_class = PurchaseSerializer
    filterset_class = PurchaseFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return PurchaseGetSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)
