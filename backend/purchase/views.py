from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from purchase.serializers import (
    PurchaseSerializer,
    PurchaseGetSerializer,
    PurchaseGetAdminSerializer,
    PaymentSerializer,
    ServicePurchaseSerializer,
    ServicePurchaseGetSerializer,
)
from purchase.models import Purchase, ServicePurchase, Payment
from purchase.filters import PurchaseFilter, ServicePurchaseFilter, PaymentFilter
from purchase.utils import (
    get_lessons_price,
    get_total_price,
    get_discount_percentage,
    get_discounted_total,
    discount_lesson_price,
    confirm_purchase,
)
from profile.models import Profile, StudentProfile, OtherProfile
from profile.models import Profile
from coupon.models import Coupon, CouponUser
from coupon.validation import validate_coupon
from utils.przelewy24.payment import Przelewy24Api
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Prefetch
from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase.utils import confirm_service_purchase
from const import PaymentMethod, PaymentStatus
import json


class PurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = (
        Purchase.objects.add_meeting_url()
        .add_recordings_ids()
        .add_reservation_id()
        .add_review_id()
        .add_lesson_status()
        .add_review_status()
        .all()
        .order_by("id")
    )
    serializer_class = PurchaseGetSerializer
    filterset_class = PurchaseFilter
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return PurchaseGetAdminSerializer
        return self.serializer_class

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:
            queryset = self.queryset.filter(
                student__profile__user=user, payment__status=PaymentStatus.SUCCESS
            )
        else:
            queryset = self.queryset

        lecturer_id = self.request.query_params.get("lecturer_id", None)
        sort_by = self.request.query_params.get("sort_by", None)
        if lecturer_id:
            return queryset.add_lecturer_id()
        if sort_by:
            if "lecturer_id" in sort_by:
                return queryset.add_lecturer_id()

        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        data = request.data

        lessons = data.pop("lessons")
        lessons = get_lessons_price(lessons=lessons)

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
                total=get_total_price(lessons=lessons) * 100,
            )
            if not valid:
                raise ValidationError({"coupon": error_message})

            # use coupon
            coupon_obj = Coupon.objects.get(code=coupon_code)
            coupon_details = {
                "discount": coupon_obj.discount,
                "is_percentage": coupon_obj.is_percentage,
            }

            discount_percentage = get_discount_percentage(
                lessons=lessons_data, coupon_details=coupon_details
            )

            records = discount_lesson_price(
                lessons=lessons_data, discount_percentage=discount_percentage
            )
            total = get_discounted_total(
                total_price=get_total_price(lessons=lessons_data),
                coupon_details=coupon_details,
            )
        else:
            records = lessons_data
            total = get_total_price(lessons=records)

        # initialize payment record
        payment = Payment.objects.create(
            amount=total * 100, method=PaymentMethod.PRZELEWY24
        )

        if coupon_code != "":
            CouponUser.objects.create(
                user=StudentProfile.objects.get(profile=profile),
                coupon=coupon_obj,
                payment=payment,
            )

        # create records
        serializer = PurchaseSerializer(
            data=records, context={"request": request, "payment": payment.id}
        )
        instances = serializer.create(serializer.initial_data)

        if total == 0:
            payment.status = PaymentStatus.SUCCESS
            payment.save()
            status_code = status.HTTP_200_OK
            data = {"token": ""}
            purchases = Purchase.objects.filter(payment=payment)
            confirm_purchase(purchases=purchases, payment=payment)
        else:
            # register payment
            przelewy24 = Przelewy24Api(payment=payment)
            register_result = przelewy24.register(client=profile, purchases=instances)
            status_code = register_result["status_code"]
            data = register_result["data"]

        return JsonResponse(
            status=status_code,
            data=data,
        )


class PaymentVerifyAPIView(APIView):
    http_method_names = ["post"]

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        session_id = data.get("sessionId")
        order_id = data.get("orderId")
        amount = data.get("amount")

        payment = Payment.objects.filter(session_id=session_id, amount=amount).first()

        if not payment:
            return JsonResponse(
                {"status": "failure"}, status=status.HTTP_400_BAD_REQUEST
            )

        payment.order_id = order_id
        przelewy24 = Przelewy24Api(payment=payment)
        verification_success = przelewy24.verify()

        payment.status = (
            PaymentStatus.SUCCESS if verification_success else PaymentStatus.FAILURE
        )
        payment.save()

        if verification_success:
            return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)
        return JsonResponse(
            {"status": "failure"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class PaymentStatusViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Purchase.objects.all().order_by("id")
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        self.queryset = self.queryset.filter(student__profile__user=user)

        session_id = request.query_params.get("session_id")

        purchases = self.queryset.filter(payment__session_id=session_id)
        if not purchases.exists():
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "Nie znaleziono."},
            )

        purchase = purchases.first()
        payment = purchase.payment

        if payment.status == "P":
            payment.status = "F"
            payment.save()

        serializer = PaymentSerializer(instance=payment)
        data = serializer.data

        confirm_purchase(purchases=purchases, payment=payment)

        return Response(data)


class PaymentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Payment.objects.all().order_by("id")
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def is_valid(self, instance: Payment):
        return not Purchase.objects.filter(payment=instance).exists()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not self.is_valid(instance=instance):
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                data={"root": "Nie można edytować tej płatności."},
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not self.is_valid(instance=instance):
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                data={"root": "Nie można usunąć tej płatności."},
            )

        return super().destroy(request, *args, **kwargs)


class ServicePurchaseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = (
        ServicePurchase.objects.prefetch_related(
            Prefetch("other", queryset=OtherProfile.objects.add_full_name())
        )
        .all()
        .order_by("id")
    )
    serializer_class = ServicePurchaseSerializer
    filterset_class = ServicePurchaseFilter
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ServicePurchaseGetSerializer
        return self.serializer_class


@receiver([post_save], sender=ServicePurchase)
def check_total_purchase_amount(sender, instance: ServicePurchase, **kwargs):
    payment = instance.payment
    purchases = ServicePurchase.objects.filter(payment=payment)

    total_price = purchases.aggregate(Sum("price"))["price__sum"]

    if total_price == payment.amount / 100:
        confirm_service_purchase(purchases=purchases, payment=payment)
