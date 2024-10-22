from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from wishlist.serializers import WishlistSerializer, WishlistGetSerializer
from wishlist.models import Wishlist
from django.db.models import Prefetch
from lesson.models import Lesson


class WishlistViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Wishlist.objects.prefetch_related(
        Prefetch("lesson", queryset=Lesson.objects.add_lecturers_ids().all())
    ).order_by("id")
    serializer_class = WishlistGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(student__profile__user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return WishlistSerializer
        return self.serializer_class
