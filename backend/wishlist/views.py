from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from wishlist.serializers import WishlistSerializer, WishlistGetSerializer
from wishlist.models import Wishlist
from profile.models import Profile


class WishlistViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Wishlist.objects.all()
    serializer_class = WishlistGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)

    def get_serializer_class(self):
        if self.action == "create":
            return WishlistSerializer
        else:
            return self.serializer_class
