from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = CartSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=CartGetSerializer(records, many=True).data,
        )
