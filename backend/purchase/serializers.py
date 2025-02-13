from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
    ImageField,
    ValidationError,
)
from django.db.models import Prefetch, Sum
from purchase.models import Purchase, ServicePurchase, Payment
from lesson.models import Lesson, Technology
from service.models import Service
from profile.models import Profile, LecturerProfile, StudentProfile, OtherProfile
from reservation.models import Reservation
from schedule.models import Schedule, Recording
from review.models import Review


class TechnologySerializer(ModelSerializer):
    class Meta:
        model = Technology
        exclude = (
            "description",
            "modified_at",
            "created_at",
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        exclude = (
            "active",
            "technologies",
            "description",
            "price",
            "modified_at",
            "created_at",
        )


class LecturerSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, lecturer: LecturerProfile):
        return lecturer.full_name


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        exclude = (
            "student",
            "lecturer",
            "modified_at",
            "created_at",
            "lesson",
        )


class ScheduleSerializer(ModelSerializer):
    lecturer = LecturerSerializer()

    class Meta:
        model = Schedule
        exclude = (
            "lesson",
            "created_at",
            "modified_at",
        )


class ReservationSerializer(ModelSerializer):
    schedule = ScheduleSerializer()

    class Meta:
        model = Reservation
        exclude = (
            "student",
            "lesson",
            "created_at",
            "modified_at",
        )


class RecordingSerializer(ModelSerializer):
    class Meta:
        model = Recording
        fields = (
            "file_name",
            "file_url",
        )


class PurchaseGetSerializer(ModelSerializer):
    lesson = LessonSerializer()
    lesson_status = SerializerMethodField()
    reservation = SerializerMethodField()
    review_status = SerializerMethodField()
    review = SerializerMethodField()
    meeting_url = SerializerMethodField()
    recordings = SerializerMethodField()
    payment = SerializerMethodField()

    class Meta:
        model = Purchase
        exclude = (
            "student",
            "modified_at",
        )

    def get_meeting_url(self, purchase: Purchase):
        return purchase.meeting_url

    def get_recordings(self, purchase: Purchase):
        if purchase.recordings_ids == []:
            return None
        recordings = Recording.objects.filter(id__in=purchase.recordings_ids)
        return RecordingSerializer(recordings, many=True).data

    def get_lesson_status(self, purchase: Purchase):
        return purchase.lesson_status

    def get_review_status(self, purchase: Purchase):
        return purchase.review_status

    def get_reservation(self, purchase: Purchase):
        if not purchase.reservation_id:
            return None

        reservation = Reservation.objects.prefetch_related(
            Prefetch(
                "schedule__lecturer", queryset=LecturerProfile.objects.add_full_name()
            )
        ).get(id=purchase.reservation_id)
        return ReservationSerializer(reservation).data

    def get_review(self, purchase: Purchase):
        if not purchase.review_id:
            return None

        review = Review.objects.get(id=purchase.review_id)
        return ReviewSerializer(review).data

    def get_payment(self, purchase: Purchase):
        return Payment.objects.get(id=purchase.payment_id).session_id


class PurchaseGetAdminSerializer(ModelSerializer):
    lesson = LessonSerializer()
    payment = SerializerMethodField()

    class Meta:
        model = Purchase
        exclude = ("student",)

    def get_payment(self, purchase: Purchase):
        return Payment.objects.get(id=purchase.payment_id).session_id


class PurchaseSerializer(ModelSerializer):
    class Meta:
        model = Purchase
        exclude = ("student", "payment")

    def validate_lesson(self, lesson):
        if not lesson.active:
            raise ValidationError("Lekcja jest nieaktywna.")

        return lesson

    def create(self, validated_data):
        user = self.context["request"].user
        student = Profile.objects.get(user=user)

        payment_id = self.context["payment"]
        payment = Payment.objects.get(pk=payment_id)

        objs = []
        for data in validated_data:
            lesson = Lesson.objects.get(id=data["lesson"])
            obj = Purchase.objects.create(
                lesson=lesson,
                price=data["price"],
                student=StudentProfile.objects.get(profile=student),
                payment=payment,
            )
            objs.append(obj)

        return objs


class PaymentSerializer(ModelSerializer):
    status = CharField(source="get_status_display")

    class Meta:
        model = Payment
        exclude = ("modified_at",)

    def create(self, validated_data):
        status = validated_data.pop("get_status_display")

        payment = Payment.objects.create(status=status, **validated_data)

        return payment

    def update(self, instance: Payment, validated_data):
        status = validated_data.pop("get_status_display")

        Payment.objects.filter(pk=instance.pk).update(status=status, **validated_data)

        instance.refresh_from_db()

        return instance


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        exclude = (
            "active",
            "description",
            "price",
            "modified_at",
            "created_at",
        )


class OtherSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    gender = CharField(source="profile.get_gender_display")
    image = ImageField(source="profile.image")

    class Meta:
        model = LecturerProfile
        fields = (
            "id",
            "full_name",
            "gender",
            "image",
        )

    def get_full_name(self, other: OtherProfile):
        return other.full_name


class ServicePurchaseGetSerializer(ModelSerializer):
    service = ServiceSerializer()
    other = OtherSerializer()
    payment = SerializerMethodField()

    class Meta:
        model = ServicePurchase
        exclude = ("modified_at",)

    def get_payment(self, purchase: Purchase):
        return Payment.objects.get(id=purchase.payment_id).session_id


class ServicePurchaseSerializer(ModelSerializer):
    class Meta:
        model = ServicePurchase
        fields = "__all__"

    def validate(self, data):
        service = data["service"]
        price = data["price"]
        payment = data["payment"]

        self.validate_payment_amount(price=price, payment=payment)
        self.validate_service(service=service)

        return data

    def validate_payment_amount(self, price, payment: Payment):
        amount = payment.amount / 100
        purchases = Purchase.objects.filter(payment=payment).all()
        total = purchases.aggregate(Sum("price"))["price__sum"] or 0

        if float(total) + float(price) > amount:
            raise ValidationError(
                {"price": "Cena usługi przekracza wartość płatności."}
            )

        return price

    def validate_service(self, service: Service):
        if not service.active:
            raise ValidationError("Usługa jest nieaktywna.")

        return service
