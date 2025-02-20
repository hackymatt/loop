from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    CharField,
)
from coupon.models import Coupon, CouponUser
from profile.models import StudentProfile
from notification.utils import notify
from typing import List


def notify_users(users: List[StudentProfile], coupon: Coupon):
    if coupon.active:
        discount_type = "%" if coupon.is_percentage else " zł"
        for user in users:
            notify(
                profile=user.profile,
                title=f"Otrzymujesz nowy kupon zniżkowy na -{coupon.discount}{discount_type}",
                subtitle=coupon.code,
                description=f"Wykorzystaj powyższy kupon do {coupon.expiration_date.strftime('%d-%m-%Y')}.",
                path="",
                icon="mdi:coupon",
            )


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


class StudentSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.gender")

    class Meta:
        model = StudentProfile
        fields = (
            "id",
            "full_name",
            "email",
            "gender",
        )

    def get_full_name(self, student: StudentProfile):
        return student.full_name


class CouponGetSerializer(ModelSerializer):
    users = StudentSerializer(many=True)

    class Meta:
        model = Coupon
        fields = "__all__"


class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"

    def add_users(self, coupon, users):
        for user in users:
            coupon.users.add(user)

        return coupon

    def create(self, validated_data):
        users = validated_data.pop("users")

        coupon = Coupon.objects.create(**validated_data)
        coupon = self.add_users(coupon=coupon, users=users)
        coupon.save()

        notify_users(users=users, coupon=coupon)

        if coupon.all_users:
            notify_users(users=StudentProfile.objects.all(), coupon=coupon)

        return coupon

    def update(self, instance: Coupon, validated_data):
        users = validated_data.pop("users", instance.users)

        Coupon.objects.filter(pk=instance.pk).update(**validated_data)

        instance.refresh_from_db()
        instance.users.clear()
        instance = self.add_users(coupon=instance, users=users)
        instance.save()

        notify_users(users=users, coupon=instance)

        if instance.all_users:
            notify_users(users=StudentProfile.objects.all(), coupon=instance)

        return instance


class CouponUserSerializer(ModelSerializer):
    user = StudentSerializer()
    coupon = CouponListSerializer()

    class Meta:
        model = CouponUser
        fields = "__all__"
