from backend.base_model import BaseModel
from django.db.models import (
    ForeignKey,
    ManyToManyField,
    BooleanField,
    BigIntegerField,
    IntegerField,
    DateTimeField,
    DecimalField,
    CharField,
    CASCADE,
)
from django.core.validators import (
    MinValueValidator,
)
from decimal import Decimal
from profile.models import Profile


class AllowedUsersRule(BaseModel):
    users = ManyToManyField(Profile, blank=True)
    all_users = BooleanField(default=False)

    class Meta:
        db_table = "coupon_allowed_users_rule"
        ordering = ["id"]


class MaxUsageRule(BaseModel):
    max_uses = BigIntegerField(default=0)
    is_infinite = BooleanField(default=False)
    uses_per_user = IntegerField(default=1)

    class Meta:
        db_table = "coupon_usage_rule"
        ordering = ["id"]


class ValidityRule(BaseModel):
    expiration_date = DateTimeField()
    is_active = BooleanField(default=False)

    class Meta:
        db_table = "coupon_validity_rule"
        ordering = ["id"]


class MinPurchaseTotalRule(BaseModel):
    min_total = DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=0,
    )

    class Meta:
        db_table = "coupon_min_purchase_total_rule"
        ordering = ["id"]


class Rules(BaseModel):
    allowed_users = ForeignKey(AllowedUsersRule, on_delete=CASCADE)
    max_usage = ForeignKey(MaxUsageRule, on_delete=CASCADE)
    validity = ForeignKey(ValidityRule, on_delete=CASCADE)
    min_purchase_total = ForeignKey(MinPurchaseTotalRule, on_delete=CASCADE)

    class Meta:
        db_table = "coupon_rules"
        ordering = ["id"]


class Discount(BaseModel):
    value = IntegerField(default=0)
    is_percentage = BooleanField(default=False)

    class Meta:
        db_table = "coupon_discount"
        ordering = ["id"]


class Coupon(BaseModel):
    code = CharField(
        max_length=36,
        unique=True,
    )
    discount = ForeignKey(Discount, on_delete=CASCADE)
    times_used = IntegerField(default=0)

    rules = ForeignKey(Rules, on_delete=CASCADE)


class CouponUser(BaseModel):
    user = ForeignKey(Profile, on_delete=CASCADE)
    coupon = ForeignKey(Coupon, on_delete=CASCADE)
    times_used = IntegerField(default=0)

    class Meta:
        db_table = "coupon_user"
        ordering = ["id"]
