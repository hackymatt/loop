from django.conf import settings
from zoomus import ZoomClient


class Zoom:
    def __init__(self):
        self.client = ZoomClient(
            client_id=settings.ZOOM_CLIENT_ID,
            client_secret=settings.ZOOM_CLIENT_SECRET,
            api_account_id=settings.ZOOM_ACCOUNT_ID,
        )

    @property
    def group(self):
        return ZoomGroup()

    @property
    def user(self):
        return ZoomUser()

    @property
    def meeting(self):
        return ZoomMeeting()


class ZoomGroup(Zoom):
    def __init__(self):
        super().__init__()

    def list(self):
        # scope: group:read:list_groups:admin
        return self.client.group.list()

    def get(self, group_id):
        # scope: group:read:group:admin
        return self.client.group.get(id=group_id)

    def create(self, group_name):
        # scope: group:write:group:admin
        return self.client.group.create(name=group_name)

    def get_or_create(self, group_id, group_name):
        group = self.group.get(group_id=group_id)
        created = False
        if not group.ok:
            group = self.group.create(group_name=group_name)
            created = True

        return created, group

    def add_member(self, group_id, users):
        # scope: group:write:member:admin
        group_members = []
        for user in users:
            zoom_user = self.user.get(user_id=user)
            if zoom_user.ok:
                content = zoom_user.json()
                group_members.append({"id": content["id"], "email": content["email"]})

        return self.client.group.add_members(groupid=group_id, members=group_members)

    def delete_member(self, group_id, member_id):
        # scope: group:delete:member:admin
        return self.client.group.delete_member(groupid=group_id, memberid=member_id)

    def list_members(self, group_id):
        # scope: group:read:list_members:admin
        return self.client.group.list_members(groupid=group_id)


class ZoomUser(Zoom):
    def __init__(self):
        super().__init__()

    def list(self):
        # scope: user:read:list_users:admin
        return self.client.user.list()

    def get(self, user_id):
        # scope: user:read:user
        return self.client.user.get(id=user_id)

    def create(self, email, first_name, last_name, display_name=""):
        # scope: user:write:user:admin
        if display_name == "":
            display_name = f"{first_name} {last_name}"
        return self.client.user.create(
            action="create",
            user_info={
                "type": 2,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "display_name": display_name,
            },
        )

    def get_or_create(self, user_id, email, first_name, last_name, display_name=""):
        user = self.user.get(user_id=user_id)
        created = False
        if not user.ok:
            user = self.user.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
            )
            created = True

        return created, user

    def delete(self, user_id):
        # scope: user:delete:user:admin
        return self.client.user.delete(action="disassociate", id=user_id)


class ZoomMeeting(Zoom):
    def __init__(self):
        super().__init__()

    def list(self, user_id):
        # scope: meeting:read:list_meetings:admin
        return self.client.meeting.list(user_id=user_id)

    def get(self, meeting_id):
        # scope: meeting:read:meeting:admin
        return self.client.meeting.get(id=meeting_id)

    def create(self, user_id, topic, agenda, duration, start_time):
        # scope: meeting:write:meeting:admin
        return self.client.meeting.create(
            user_id=user_id,
            topic=topic,
            agenda=agenda,
            start_time=start_time,
            timezone="UTC",
            duration=duration,
            type=2,
            settings={
                "allow_multiple_devices": False,
                "auto_recording": "cloud",
                "mute_upon_entry": True,
                "registrants_confirmation_email": True,
                "registration_type": 2,
                "approval_type": 0,
            },
        )

    def delete(self, meeting_id):
        # scope: meeting:delete:meeting:admin
        return self.client.meeting.delete(id=meeting_id)

    def list_registrants(self, meeting_id):
        # scope: meeting:read:list_registrants:admin
        return self.client.meeting.list_registrants(id=meeting_id)

    def add_registrant(self, meeting_id, email, first_name, last_name):
        # scope: meeting:write:registrant:admin
        return self.client.meeting.add_registrant(
            id=meeting_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            language="pl-PL",
        )

    def update_registrant_status(self, meeting_id, users):
        # scope: meeting:update:registrant_status:admin
        registrants = []
        for user in users:
            zoom_user = self.user.get(user_id=user)
            if zoom_user.ok:
                content = zoom_user.json()
                registrants.append({"id": content["id"], "email": content["email"]})

        return self.client.meeting.update_registrant_status(
            id=meeting_id, registrants=registrants, action="cancel"
        )


# zoom = Zoom()
# print(zoom.group.list())
# print(zoom.group.get(group_id="825c9e31f1064c73b394c5e4557d3447"))
# print(zoom.group.create(group_name="lecturers"))
# print(zoom.group.get_or_create(group_id="825c9e31f1064c73b394c5e4557d3447", group_name="lecturers"))
# print(zoom.group.add_member(group_id="825c9e31f1064c73b394c5e4557d3447", users=["matios94@gmail.com"]))
# print(zoom.group.delete_member(group_id="825c9e31f1064c73b394c5e4557d3447", member_id="matios94@gmail.com"))
# print(zoom.group.list_members(group_id="825c9e31f1064c73b394c5e4557d3447"))
# print(zoom.user.list())
# print(zoom.user.get(user_id="matios94@gmail.com").json())
# print(zoom.user.create(email="matios94@yahoo.com", first_name="Adam", last_name="Lewicki"))
# print(zoom.user.get_or_create(user_id="matios94@gmail.com", email="matios94@gmail.com", first_name="Adam",
#                               last_name="Lewicki"))
# print(zoom.user.delete(user_id="matios94@yahoo.com"))
# print(zoom.meeting.list(user_id="matios94@gmail.com"))
# print(zoom.meeting.get(meeting_id=78474388740).json())
# print(zoom.meeting.create(user_id="matios94@gmail.com", topic="JavaScript for beginners", agenda="Testing", duration=30, start_time=datetime.datetime.now()).json())
# print(zoom.meeting.delete(meeting_id=72006179014))
# print(zoom.meeting.list_registrants(meeting_id=73480512329).json())
# print(zoom.meeting.add_registrant(meeting_id=78474388740, email="matios94@yahoo.com", first_name="Adam", last_name="Lewicki").json())
# print(zoom.meeting.update_registrant_status(meeting_id=78474388740, users=["matios94@gmail.com"]))
