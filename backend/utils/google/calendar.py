from utils.google.service import build_service
import uuid
from config_global import MEETINGS_EMAIL


class CalendarApi:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/calendar.events"]
        self.service = build_service(
            service_name="calendar",
            service_version="v3",
            on_behalf_of=MEETINGS_EMAIL,
            scopes=scopes,
        )

    def _create_event(
        self, title, description, start_time, end_time, lecturer, students
    ):
        lecturer_full_name = lecturer["full_name"]
        attendees = [
            {
                "email": student["email"],
                "displayName": student["full_name"],
                "responseStatus": "accepted",
            }
            for student in students
        ]
        return {
            "kind": "calendar#event",
            "status": "confirmed",
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Europe/London",
            },
            "attendees": [
                {
                    "email": lecturer["email"],
                    "displayName": f"{lecturer_full_name} (Instruktor)",
                    "responseStatus": "accepted",
                },
                *attendees,
            ],
            "guestsCanInviteOthers": False,
            "guestsCanSeeOtherGuests": False,
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 15},
                ],
            },
            "eventType": "default",
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                },
            },
        }

    def create(self, title, description, start_time, end_time, lecturer, students):
        event = self._create_event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            lecturer=lecturer,
            students=students,
        )
        return (
            self.service.events()
            .insert(
                calendarId="primary",
                body=event,
                conferenceDataVersion=1,
                sendUpdates="none",
            )
            .execute()
        )

    def update(
        self, event_id, title, description, start_time, end_time, lecturer, students
    ):
        event = self._create_event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            lecturer=lecturer,
            students=students,
        )
        return (
            self.service.events()
            .update(
                calendarId="primary",
                eventId=event_id,
                body=event,
                sendUpdates="none",
            )
            .execute()
        )

    def delete(self, event_id):
        return (
            self.service.events()
            .delete(calendarId="primary", eventId=event_id, sendUpdates="none")
            .execute()
        )
