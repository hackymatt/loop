from rest_framework.serializers import ModelSerializer
from coupon.models import Coupon


class CouponListSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "discount",
            "is_percentage",
            "active",
            "expiration_date",
        )


class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "discount",
            "is_percentage",
            "active",
            "expiration_date",
        )
