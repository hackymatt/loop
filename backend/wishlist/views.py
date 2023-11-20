from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from wishlist.serializers import WishlistSerializer, WishlistGetSerializer
from wishlist.models import Wishlist
from profile.models import Profile


class WishlistViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistGetSerializer

    def list(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"wishlist": "Użytkownik niezalogowany."},
            )

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"wishlist": "Użytkownik niezalogowany."},
            )

        profile = Profile.objects.get(user=user)
        data["profile"] = profile.id
        serializer = WishlistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=WishlistGetSerializer(records, many=True).data,
        )
