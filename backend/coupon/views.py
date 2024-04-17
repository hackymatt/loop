from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from coupon.serializers import (
    CouponListSerializer,
    CouponGetSerializer,
    CouponSerializer,
    CouponUserSerializer,
)
from coupon.filters import CouponFilter, CouponUserFilter
from coupon.models import Coupon, CouponUser


class CouponViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filterset_class = CouponFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return CouponListSerializer
        elif self.action == "retrieve":
            return CouponGetSerializer
        else:
            return self.serializer_class


class CouponUserViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = CouponUser.objects.all()
    serializer_class = CouponUserSerializer
    filterset_class = CouponUserFilter
    permission_classes = [IsAuthenticated, IsAdminUser]
