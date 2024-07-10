from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    EmailField,
    CharField,
)
from coupon.models import Coupon, CouponUser
from profile.models import Profile, StudentProfile


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
    full_name = SerializerMethodField("get_full_name")
    email = EmailField(source="profile.user.email")
    gender = CharField(source="profile.get_gender_display")

    class Meta:
        model = StudentProfile
        fields = (
            "id",
            "full_name",
            "email",
            "gender",
        )

    def get_full_name(self, student):
        return student.profile.user.first_name + " " + student.profile.user.last_name


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

        return coupon

    def update(self, instance, validated_data):
        users = validated_data.pop("users", instance.users)

        Coupon.objects.filter(pk=instance.pk).update(**validated_data)

        instance = Coupon.objects.get(pk=instance.pk)
        instance.users.clear()
        instance = self.add_users(coupon=instance, users=users)
        instance.save()

        return instance


class CouponUserSerializer(ModelSerializer):
    user = StudentSerializer()
    coupon = CouponListSerializer()

    class Meta:
        model = CouponUser
        fields = "__all__"
