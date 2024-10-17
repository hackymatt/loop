from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer, CartGetSerializer
from cart.models import Cart


class CartViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Cart.objects.all().select_related("student")
    serializer_class = CartGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(student__profile__user=self.request.user)

    def get_serializer_class(self):
        return CartSerializer if self.action == "create" else self.serializer_class
