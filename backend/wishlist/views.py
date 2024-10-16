from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from wishlist.serializers import WishlistSerializer, WishlistGetSerializer
from wishlist.models import Wishlist
from profile.models import Profile


class WishlistViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Wishlist.objects.all().select_related("student")
    serializer_class = WishlistGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(student__profile__user=self.request.user)

    def get_serializer_class(self):
        return WishlistSerializer if self.action == "create" else self.serializer_class
