from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from reservation.models import Reservation
from profile.models import Profile


class CertificateViewSet(ModelViewSet):
    http_method_names = ["get"]

    @csrf_exempt
    def get_certificate(request, id):
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user=user)
            authenticated_profile_uuid = profile.uuid
        else:
            authenticated_profile_uuid = ""

        profile_uuid, reservation_id = id.rsplit("-", 1)

        profile = Profile.objects.filter(uuid=profile_uuid)
        if not profile.exists():
            return JsonResponse(
                status=status.HTTP_404_NOT_FOUND,
                data={},
            )
        profile = profile.first()

        reservation = Reservation.objects.filter(
            pk=reservation_id, student__profile=profile
        )
        if not reservation.exists():
            return JsonResponse(
                status=status.HTTP_404_NOT_FOUND,
                data={},
            )
        reservation = reservation.first()

        data = {
            "reference_number": "{:05d}".format(reservation.id),
            "lesson_title": reservation.lesson.title,
            "lesson_duration": reservation.lesson.duration,
            "teacher_name": f"{reservation.schedule.lecturer.profile.user.first_name} {reservation.schedule.lecturer.profile.user.last_name}",
            "student_name": f"{reservation.student.profile.user.first_name} {reservation.student.profile.user.last_name}",
            "completion_date": reservation.schedule.start_time.date(),
        }

        if str(profile_uuid) == str(authenticated_profile_uuid):
            data = {**data, "authorized": True}

        return JsonResponse(status=status.HTTP_200_OK, data=data)
