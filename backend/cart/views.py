from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer, CartGetSerializer
from cart.models import Cart
from django.db.models import Prefetch
from lesson.models import Lesson


class CartViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Cart.objects.prefetch_related(
        Prefetch("lesson", queryset=Lesson.objects.add_lecturers_ids().all())
    ).order_by("id")
    serializer_class = CartGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(student__profile__user=user)

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CartSerializer
        return self.serializer_class
