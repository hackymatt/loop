from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from django.http import JsonResponse
from coupon.serializers import (
    CouponListSerializer,
    CouponGetSerializer,
    CouponSerializer,
    CouponUserSerializer,
)
from coupon.filters import CouponFilter, CouponUserFilter
from coupon.models import Coupon, CouponUser
from coupon.validation import validate_coupon
from profile.models import Profile, StudentProfile
from django.db.models import Prefetch


class CouponViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = (
        Coupon.objects.prefetch_related(
            Prefetch("users", queryset=StudentProfile.objects.add_full_name())
        )
        .all()
        .order_by("id")
    )
    serializer_class = CouponSerializer
    filterset_class = CouponFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return CouponListSerializer
        elif self.action == "retrieve":
            return CouponGetSerializer
        return self.serializer_class


class CouponUserViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        CouponUser.objects.prefetch_related(
            Prefetch("user", queryset=StudentProfile.objects.add_full_name())
        )
        .all()
        .order_by("id")
    )
    serializer_class = CouponUserSerializer
    filterset_class = CouponUserFilter
    permission_classes = [IsAuthenticated, IsAdminUser]


class CouponValidationAPIView(APIView):
    http_method_names = ["get"]

    def get(self, request, coupon_code, total):
        user = request.user
        profile = Profile.objects.get(user=user)

        valid, error_message = validate_coupon(
            coupon_code=coupon_code, user=profile, total=total
        )

        if not valid:
            return JsonResponse(
                status=status.HTTP_400_BAD_REQUEST,
                data={"code": error_message},
            )

        coupon = Coupon.objects.get(code=coupon_code)

        return JsonResponse(
            status=status.HTTP_200_OK,
            data={"discount": coupon.discount, "is_percentage": coupon.is_percentage},
        )
