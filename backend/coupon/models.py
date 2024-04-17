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
    MinLengthValidator,
)
from decimal import Decimal
from profile.models import Profile


class Coupon(BaseModel):
    code = CharField(max_length=36, unique=True, validators=[MinLengthValidator(6)])
    discount = IntegerField(default=0)
    is_percentage = BooleanField(default=False)
    users = ManyToManyField(Profile, blank=True)
    all_users = BooleanField(default=False)
    max_uses = BigIntegerField(default=0)
    is_infinite = BooleanField(default=False)
    uses_per_user = IntegerField(default=1)
    expiration_date = DateTimeField()
    active = BooleanField(default=False)
    min_total = DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        default=0,
    )


class CouponUser(BaseModel):
    user = ForeignKey(Profile, on_delete=CASCADE)
    coupon = ForeignKey(Coupon, on_delete=CASCADE)

    class Meta:
        db_table = "coupon_user"
        ordering = ["id"]
