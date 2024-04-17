from rest_framework.serializers import ValidationError
from coupon.models import Coupon, CouponUser
from django.utils import timezone


def validate_allowed_users(coupon, user):
    all_users = coupon.all_users
    allowed_users = coupon.allowed_users.all()

    if user not in allowed_users and not all_users:
        return ValidationError({"coupon": "Kupon jest niedostępny."})


def validate_max_usage(coupon, user):
    infinite = coupon.is_infinite
    max_usage = coupon.max_uses
    usage_per_user = coupon.uses_per_user

    current_usage = CouponUser.objects.filter(coupon=coupon).count()

    if current_usage >= max_usage and not infinite:
        return ValidationError({"coupon": "Kupon jest niedostępny."})

    user_usage = CouponUser.objects.filter(coupon=coupon, user=user).count()
    if user_usage >= usage_per_user:
        return ValidationError({"coupon": "Kupon jest niedostępny."})


def validate_validity(coupon):
    expiration_date = coupon.expiration_date
    active = coupon.active

    if timezone.now() > expiration_date:
        return ValidationError({"coupon": "Kupon wygasł."})

    if not active:
        return ValidationError({"coupon": "Kupon jest nieaktywny."})


def validate_min_total(coupon, total):
    min_total = coupon.min_total

    if total < min_total:
        return ValidationError(
            {"coupon": f"Kupon ważny dla zamówienia za min. {min_total}."}
        )


def validate_coupon(coupon_code, user, total):
    if not coupon_code:
        return ValidationError({"coupon": "Kupon jest pusty."})

    if not user:
        return ValidationError({"coupon": "Użytkownik jest niedostępny."})

    coupon = Coupon.objects.filter(code=coupon_code)

    if not coupon.exists():
        return ValidationError({"coupon": "Kupon nie istnieje."})

    validate_allowed_users(coupon=coupon, user=user)
    validate_max_usage(coupon=coupon, user=user)
    validate_validity(coupon=coupon)
    validate_min_total(coupon=coupon, total=total)
