from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from wishlist.serializers import WishlistSerializer, WishlistGetSerializer
from wishlist.models import Wishlist
from profile.models import Profile


class WishlistViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        student = Profile.objects.get(user=user)
        data["student"] = student.id
        serializer = WishlistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        records = serializer.create(serializer.data)

        return Response(
            status=status.HTTP_201_CREATED,
            data=WishlistGetSerializer(records, many=True).data,
        )
