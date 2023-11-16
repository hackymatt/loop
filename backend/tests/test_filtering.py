from rest_framework import status
from rest_framework.test import APITestCase
from .factory import (
    create_user,
    create_profile,
    create_course,
    create_lesson_obj,
    create_technology_obj,
    create_skill_obj,
    create_topic_obj,
    create_review,
    create_purchase,
    create_schedule,
)
from .helpers import get_schedules
from django.contrib import auth
import json
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class CourseFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/courses"
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_profile(user=self.user)
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Begginer",
            description="Learn Python today",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_1.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[1],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[1],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_1.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_1.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=create_technology_obj(name="Javascript"),
            level="Zaawansowany",
            price="300",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 3",
                    description="bbbb",
                    duration="130",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_2.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[1],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[2],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[1],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[2],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[2],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=create_technology_obj(name="VBA"),
            level="Ekspert",
            price="220",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_3.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_3.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_3.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_3.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )

    def test_search_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?search=JS lesson 1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 1)

    def test_rating_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_from=3.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_duration_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?filters=(duration_to=100)|(duration_from=250)"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_technology_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?technology_in=Python,VBA")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_level_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?level_in=Podstawowy,Ekspert")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_price_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?price_from=100&price_to=300")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_active_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?active=False")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 0)


class ReviewFilterTest(APITestCase):
    def setUp(self):
        self.endpoint = "/reviews"
        self.data = {
            "email": "test_email@example.com",
            "password": "TestPassword123",
        }
        self.user = create_user(
            first_name="first_name",
            last_name="last_name",
            email=self.data["email"],
            password=self.data["password"],
            is_active=True,
        )
        self.profile = create_profile(user=self.user)
        self.user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="test2@example.com",
            password="Test12345",
            is_active=True,
        )
        self.profile_2 = create_profile(user=self.user_2)
        self.lecturer_user_1 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_1@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_user_2 = create_user(
            first_name="first_name",
            last_name="last_name",
            email="lecturer_2@example.com",
            password=self.data["password"],
            is_active=True,
        )
        self.lecturer_profile_1 = create_profile(
            user=self.lecturer_user_1, user_type="W"
        )
        self.lecturer_profile_2 = create_profile(
            user=self.lecturer_user_2, user_type="W"
        )
        # course 1
        self.course_1 = create_course(
            title="Python Begginer",
            description="Learn Python today",
            technology=create_technology_obj(name="Python"),
            level="Podstawowy",
            price="99.99",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="Python lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_1.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[1],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_1.lessons.all()[1],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_1.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_1.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_1_1 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_1_2 = create_review(
            lesson=self.course_1.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_1_3 = create_review(
            lesson=self.course_1.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=3,
            review="So so lesson.",
        )

        # course 2
        self.course_2 = create_course(
            title="Javascript course for Advanced",
            description="Course for programmers",
            technology=create_technology_obj(name="Javascript"),
            level="Zaawansowany",
            price="300",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 2",
                    description="bbbb",
                    duration="30",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
                create_lesson_obj(
                    id=-1,
                    title="JS lesson 3",
                    description="bbbb",
                    duration="130",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="2.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_2.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[1],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[2],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[1],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_2.lessons.all()[2],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[1],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_2.lessons.all()[2],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_2_1 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_2_2 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="Good lesson.",
        )
        self.review_course_2_3 = create_review(
            lesson=self.course_2.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )
        self.review_course_2_4 = create_review(
            lesson=self.course_2.lessons.all()[1],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=1,
            review="So so lesson.",
        )
        self.review_course_2_5 = create_review(
            lesson=self.course_2.lessons.all()[2],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=4,
            review="So so lesson.",
        )

        # course 3
        self.course_3 = create_course(
            title="VBA course for Expert",
            description="Course for programmers",
            technology=create_technology_obj(name="VBA"),
            level="Ekspert",
            price="220",
            github_repo_link="www.example.com",
            skills=[create_skill_obj(name="coding"), create_skill_obj(name="IDE")],
            topics=[
                create_topic_obj(name="You will learn how to code"),
                create_topic_obj(name="You will learn a new IDE"),
            ],
            lessons=[
                create_lesson_obj(
                    id=-1,
                    title="VBA lesson 1",
                    description="bbbb",
                    duration="90",
                    github_branch_link="https://github.com/hackymatt/CodeEdu",
                    price="9.99",
                ),
            ],
        )

        for i in range(5):
            create_schedule(
                self.course_3.lessons.all()[0],
                self.lecturer_profile_1,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )
            create_schedule(
                self.course_3.lessons.all()[0],
                self.lecturer_profile_2,
                make_aware(
                    datetime.now().replace(second=0, microsecond=0)
                    + timedelta(minutes=30 * i)
                ),
            )

        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_3.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )
        create_purchase(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            time=get_schedules(
                lesson=self.course_3.lessons.all()[0],
                lecturer=self.lecturer_profile_1,
            )[0],
        )

        self.review_course_3_1 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile,
            lecturer=self.lecturer_profile_1,
            rating=5,
            review="Great lesson.",
        )
        self.review_course_3_2 = create_review(
            lesson=self.course_3.lessons.all()[0],
            student=self.profile_2,
            lecturer=self.lecturer_profile_1,
            rating=2,
            review="So so lesson.",
        )

    def test_course_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?course_id={self.course_1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_lesson_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lesson_id={self.course_1.lessons.all()[0].id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 2)

    def test_lecturer_id_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(
            f"{self.endpoint}?lecturer_id={self.lecturer_profile_1.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 10)

    def test_rating_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_rating_from_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_from=4.5")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 3)

    def test_rating_to_filter(self):
        # no login
        self.assertFalse(auth.get_user(self.client).is_authenticated)
        # get data
        response = self.client.get(f"{self.endpoint}?rating_to=4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        count = data["records_count"]
        self.assertEqual(count, 7)
