from typing import List
from utils.google.calendar import CalendarApi
from profile.models import LecturerProfile, StudentProfile
from datetime import datetime


class MeetingManager:
    def __init__(self):
        self.calendar_api = CalendarApi()

    def _create_lecturer(self, lecturer: LecturerProfile):
        return {
            "email": lecturer.profile.user.email,
            "full_name": f"{lecturer.profile.user.first_name} {lecturer.profile.user.last_name}",
        }

    def _create_students(self, students: List[StudentProfile]):
        return [
            {
                "email": student.profile.user.email,
                "full_name": f"{student.profile.user.first_name} {student.profile.user.last_name}",
            }
            for student in students
        ]

    def create(
        self,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        lecturer: LecturerProfile,
        students: List[StudentProfile],
    ):
        return self.calendar_api.create(
            title=title,
            description=description,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            lecturer=self._create_lecturer(lecturer=lecturer),
            students=self._create_students(students=students),
        )

    def update(
        self,
        event_id: str,
        title: str,
        description: str,
        start_time: datetime,
        end_time: datetime,
        lecturer: LecturerProfile,
        students: List[StudentProfile],
    ):
        return self.calendar_api.update(
            event_id=event_id,
            title=title,
            description=description,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            lecturer=self._create_lecturer(lecturer=lecturer),
            students=self._create_students(students=students),
        )

    def delete(self, event_id: str):
        return self.calendar_api.delete(event_id=event_id)
