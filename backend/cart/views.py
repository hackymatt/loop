from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from cart.serializers import CartSerializer, CartGetSerializer
from cart.models import Cart
from profile.models import Profile


class CartViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Cart.objects.all()
    serializer_class = CartGetSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"cart": "Użytkownik niezalogowany."},
            )

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"cart": "Użytkownik niezalogowany."},
            )

        student = Profile.objects.get(user=user)
        data["student"] = student.id
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=CartGetSerializer(records, many=True).data,
        )
