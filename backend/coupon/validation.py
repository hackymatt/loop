from coupon.models import Coupon, CouponUser
from django.utils import timezone


def validate_coupon(coupon_code, user, total):
    if not coupon_code:
        return False, "Kupon jest pusty."

    if not user:
        return False, "Użytkownik jest niedostępny."

    coupon = Coupon.objects.filter(code=coupon_code)

    if not coupon.exists():
        return False, "Kupon nie istnieje."

    coupon = coupon.first()
    all_users = coupon.all_users
    allowed_users = coupon.users.all()

    if user not in allowed_users and not all_users:
        return False, "Kupon jest niedostępny."

    infinite = coupon.is_infinite
    max_usage = coupon.max_uses
    usage_per_user = coupon.uses_per_user

    current_usage = CouponUser.objects.filter(coupon=coupon).count()

    if current_usage >= max_usage and not infinite:
        return False, "Pula dla kuponu została wyczerpana."

    user_usage = CouponUser.objects.filter(coupon=coupon, user=user).count()
    if user_usage >= usage_per_user:
        return False, "Nie możesz użyć ponownie tego kuponu."

    expiration_date = coupon.expiration_date
    active = coupon.active

    if timezone.now() > expiration_date:
        return False, "Kupon wygasł."

    if not active:
        return False, "Kupon jest nieaktywny."

    min_total = coupon.min_total

    if float(total) < float(min_total):
        return False, f"Kupon ważny dla zamówienia za min. {min_total} zł."

    return True, ""
