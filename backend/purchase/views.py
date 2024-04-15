from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from purchase.serializers import PurchaseSerializer, PurchaseGetSerializer
from purchase.models import Purchase
from purchase.filters import PurchaseFilter
from profile.models import Profile
from lesson.models import Lesson


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Purchase.objects.all()
    serializer_class = PurchaseGetSerializer
    filterset_class = PurchaseFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student=student)

    def get_lessons_price(self, lessons):
        for lesson_data in lessons:
            id = lesson_data["lesson"]
            lesson = Lesson.objects.get(id=id)
            lesson_data["price"] = lesson.price

        return lessons

    def validate_coupon(self, coupon):
        if coupon != "":
            is_valid = coupon != "incorrect"
            if not is_valid:
                raise ValidationError({"coupon": "Kod zniżkowy jest niepoprawny."})

        return coupon

    def get_total_price(self, lessons):
        return sum([float(lesson["price"]) for lesson in lessons])

    def get_discounted_total(self, total_price, coupon_details):
        if coupon_details["is_percentage"]:
            return float(total_price) * (1 - coupon_details["discount"] / 100)

        return total_price - coupon_details["discount"]

    def get_discount_percentage(self, lessons, coupon_details):
        if coupon_details["is_percentage"]:
            return coupon_details["discount"]

        total_price = self.get_total_price(lessons=lessons)
        discounted_total_price = total_price - coupon_details["discount"]
        return (1 - discounted_total_price / total_price) * 100

    def discount_lesson_price(self, lessons, discount_percentage):
        for lesson_data in lessons:
            original_price = lesson_data["price"]
            new_price = float(original_price) * (1 - discount_percentage / 100)
            lesson_data["price"] = round(new_price, 2)

        return lessons

    def create(self, request, *args, **kwargs):
        data = request.data

        lessons = data.pop("lessons")
        lessons = self.get_lessons_price(lessons=lessons)

        coupon = data.pop("coupon")

        serializer = PurchaseSerializer(
            data=lessons, many=True, context={"request": request}
        )
        if not serializer.is_valid():
            raise ValidationError({"lessons": serializer.errors})

        lessons_data = [dict(item) for item in serializer.data]
        self.validate_coupon(coupon=coupon)

        # use coupon
        if coupon == "value":
            coupon_details = {"discount": 1.3, "is_percentage": False}
        else:
            coupon_details = {"discount": 10, "is_percentage": True}

        discount_percentage = self.get_discount_percentage(
            lessons=lessons_data, coupon_details=coupon_details
        )

        records = self.discount_lesson_price(
            lessons=lessons_data, discount_percentage=discount_percentage
        )

        # make payment
        total = self.get_discounted_total(
            total_price=self.get_total_price(lessons=records),
            coupon_details=coupon_details,
        )
        is_payment_successful = total > 1
        if not is_payment_successful:
            raise ValidationError({"payment": "Płatność odrzucona."})

        # create records
        serializer = PurchaseSerializer(data=records, context={"request": request})
        instances = serializer.create(serializer.initial_data)

        return Response(
            status=status.HTTP_200_OK,
            data=PurchaseGetSerializer(instances, many=True).data,
        )
