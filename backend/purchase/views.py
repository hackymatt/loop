from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from purchase.serializers import (
    PurchaseSerializer,
    PurchaseGetSerializer,
    PaymentSerializer,
)
from purchase.models import Purchase, Payment
from purchase.filters import PurchaseFilter
from profile.models import Profile, StudentProfile
from profile.models import Profile
from lesson.models import Lesson
from coupon.models import Coupon, CouponUser
from coupon.validation import validate_coupon
from utils.przelewy24.payment import Przelewy24Api
from django.views.decorators.csrf import csrf_exempt
import json
from uuid import UUID


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Purchase.objects.filter(payment__status="S").all()
    serializer_class = PurchaseGetSerializer
    filterset_class = PurchaseFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = Profile.objects.get(user=user)
        return self.queryset.filter(student__profile=student)

    def get_lessons_price(self, lessons):
        for lesson_data in lessons:
            id = lesson_data["lesson"]
            lesson = Lesson.objects.get(id=id)
            lesson_data["price"] = lesson.price

        return lessons

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
        user = request.user
        profile = Profile.objects.get(user=user)
        data = request.data

        lessons = data.pop("lessons")
        lessons = self.get_lessons_price(lessons=lessons)

        coupon_code = data.pop("coupon")

        serializer = PurchaseSerializer(
            data=lessons, many=True, context={"request": request}
        )
        if not serializer.is_valid():
            raise ValidationError({"lessons": serializer.errors})

        lessons_data = [dict(item) for item in serializer.data]

        if coupon_code != "":
            valid, error_message = validate_coupon(
                coupon_code=coupon_code,
                user=profile,
                total=self.get_total_price(lessons=lessons) * 100,
            )
            if not valid:
                raise ValidationError({"coupon": error_message})

            # use coupon
            coupon_obj = Coupon.objects.get(code=coupon_code)
            CouponUser.objects.create(
                user=StudentProfile.objects.get(profile=profile), coupon=coupon_obj
            )
            coupon_details = {
                "discount": coupon_obj.discount,
                "is_percentage": coupon_obj.is_percentage,
            }

            discount_percentage = self.get_discount_percentage(
                lessons=lessons_data, coupon_details=coupon_details
            )

            records = self.discount_lesson_price(
                lessons=lessons_data, discount_percentage=discount_percentage
            )
            total = self.get_discounted_total(
                total_price=self.get_total_price(lessons=records),
                coupon_details=coupon_details,
            )
        else:
            records = lessons_data
            total = self.get_total_price(lessons=records)

        # initialize payment record
        payment = Payment.objects.create(amount=total * 100)

        # create records
        serializer = PurchaseSerializer(
            data=records, context={"request": request, "payment": payment.id}
        )
        instances = serializer.create(serializer.initial_data)

        # register payment
        przelewy24 = Przelewy24Api(payment=payment)
        register_result = przelewy24.register(client=profile, purchases=instances)

        return JsonResponse(
            status=register_result["status_code"],
            data=register_result["data"],
        )


class PaymentVerifyViewSet(ModelViewSet):
    http_method_names = ["post"]

    @csrf_exempt
    def verify_payment(request):
        print(request)
        data = json.loads(request.body)
        print(data)

        session_id = data.get("sessionId")
        order_id = data.get("orderId")
        amount = data.get("amount")

        payments = Payment.objects.filter(session_id=session_id, amount=amount)

        if not payments.exists():
            return JsonResponse(
                {"status": "failure"}, status=status.HTTP_400_BAD_REQUEST
            )

        payment = payments.first()
        payment.order_id = order_id
        przelewy24 = Przelewy24Api(payment=payment)
        verification_success = przelewy24.verify()

        payment.status = "S" if verification_success else "F"
        payment.save()

        if verification_success:
            return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
        return JsonResponse({"status": "failure"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Purchase.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        student = Profile.objects.get(user=user)
        self.queryset = self.queryset.filter(student__profile=student)

        session_id = request.query_params.get("session_id")

        purchases = self.queryset.filter(payment__session_id=session_id)
        if not purchases.exists():
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Nie znaleziono."},
            )

        purchase = purchases.first()
        payment = purchase.payment

        serializer = PaymentSerializer(instance=payment)
        data = serializer.data

        return Response(data)
