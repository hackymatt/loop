from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from purchase.serializers import PurchaseSerializer
from purchase.models import LessonPurchase
from profile.models import Profile


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = LessonPurchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)
