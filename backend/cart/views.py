from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer, CartGetSerializer
from cart.models import Cart
from profile.models import Profile


class CartViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Cart.objects.all()
    serializer_class = CartGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)

    def get_serializer_class(self):
        if self.action == "create":
            return CartSerializer
        else:
            return self.serializer_class
