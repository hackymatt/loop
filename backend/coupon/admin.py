from django.contrib import admin
from .models import (
    Coupon,
    CouponUser,
    Rules,
    MaxUsageRule,
    AllowedUsersRule,
    Discount,
    MinPurchaseTotalRule,
    ValidityRule,
)

admin.site.register(Coupon)
admin.site.register(CouponUser)
admin.site.register(Rules)
admin.site.register(MaxUsageRule)
admin.site.register(AllowedUsersRule)
admin.site.register(Discount)
admin.site.register(MinPurchaseTotalRule)
admin.site.register(ValidityRule)
