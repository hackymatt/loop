from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from coupon.serializers import (
    CouponListSerializer,
    CouponSerializer,
)
from coupon.filters import CouponFilter
from coupon.models import Coupon


class CouponViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filterset_class = CouponFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return CouponListSerializer
        else:
            return self.serializer_class
