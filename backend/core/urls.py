from profile.users.views import UserViewSet
from profile.register.views import ProfileRegisterViewSet
from profile.unregister.views import ProfileUnregisterViewSet
from profile.verify.views import ProfileVerificationCodeViewSet, ProfileVerifyViewSet
from profile.login.views import (
    EmailLoginViewSet,
    GoogleLoginViewSet,
    FacebookLoginViewSet,
    GithubLoginViewSet,
)
from profile.logout.views import ProfileLogoutViewSet
from profile.password_change.views import ProfilePasswordChangeViewSet
from profile.password_reset.views import ProfilePasswordResetViewSet
from profile.personal_data.views import PersonalDataViewSet
from profile.profile_data.views import ProfileDataViewSet
from profile.lecturers.views import LecturerViewSet, BestLecturerViewSet
from profile.earnings.views import EarningViewSet
from profile.certificate.views import CertificateViewSet
from django.urls import path, include
from django.contrib import admin
from course.views import (
    CourseViewSet,
    BestCourseViewSet,
)
from lesson.views import (
    LessonViewSet,
    LessonPriceHistoryViewSet,
)
from module.views import ModuleViewSet
from technology.views import TechnologyViewSet, BestTechnologyViewSet
from topic.views import TopicViewSet
from skill.views import SkillViewSet
from review.views import ReviewViewSet, ReviewStatsViewSet, BestReviewViewSet
from newsletter.views import (
    NewsletterEntriesViewSet,
    NewsletterSubscribeViewSet,
    NewsletterUnsubscribeViewSet,
)
from schedule.views import ManageScheduleViewSet, ScheduleViewSet
from stats.views import StatsViewSet
from wishlist.views import WishlistViewSet
from cart.views import CartViewSet
from purchase.views import PurchaseViewSet
from teaching.views import ManageTeachingViewSet, TeachingViewSet
from reservation.views import ReservationViewSet
from contact.views import ContactViewSet
from finance.views import FinanceDetailsViewSet, FinanceHistoryViewSet
from coupon.views import CouponViewSet, CouponUserViewSet, CouponValidationViewSet
from .routers import Router

router = Router(trailing_slash=False)

router.register(r"users", UserViewSet, basename="users")
router.register(r"register", ProfileRegisterViewSet, basename="user_register")
router.register(r"verify", ProfileVerifyViewSet, basename="user_verification")
router.register(r"login", EmailLoginViewSet, basename="user_login")
router.register(r"logout", ProfileLogoutViewSet, basename="user_logout")
router.register(
    r"password-change", ProfilePasswordChangeViewSet, basename="user_password_change"
)
router.register(
    r"password-reset", ProfilePasswordResetViewSet, basename="user_password_reset"
)
router.register(
    r"verify-code", ProfileVerificationCodeViewSet, basename="user_verification_code"
)
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"best-courses", BestCourseViewSet, basename="best_courses")
router.register(r"modules", ModuleViewSet, basename="modules")
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(
    r"lesson-price-history", LessonPriceHistoryViewSet, basename="lesson_price_history"
)
router.register(r"technologies", TechnologyViewSet, basename="technologies")
router.register(
    r"best-technologies", BestTechnologyViewSet, basename="best_technologies"
)
router.register(r"topics", TopicViewSet, basename="topics")
router.register(r"skills", SkillViewSet, basename="skills")
router.register(r"best-lecturers", BestLecturerViewSet, basename="best_lecturers")
router.register(r"lecturers", LecturerViewSet, basename="lecturers")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"reviews-stats", ReviewStatsViewSet, basename="reviews-stats")
router.register(r"best-reviews", BestReviewViewSet, basename="best_reviews")
router.register(r"schedules", ManageScheduleViewSet, basename="schedules")
router.register(r"lesson-schedules", ScheduleViewSet, basename="lesson_schedules")
router.register(r"newsletter", NewsletterEntriesViewSet, basename="newsletter")
router.register(r"wishlist", WishlistViewSet, basename="wishlist")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"purchase", PurchaseViewSet, basename="purchase")
router.register(r"teaching", ManageTeachingViewSet, basename="teaching")
router.register(r"lesson-lecturers", TeachingViewSet, basename="lesson_lecturers")
router.register(r"reservation", ReservationViewSet, basename="reservation")
router.register(r"finance-history", FinanceHistoryViewSet, basename="finance_history")
router.register(r"earnings", EarningViewSet, basename="earnings")
router.register(r"coupons", CouponViewSet, basename="coupons")
router.register(r"coupon-usage", CouponUserViewSet, basename="coupon_usage")

api_urlpatterns = [
    path("", include(router.urls)),
    path(
        "personal-data",
        PersonalDataViewSet.as_view({"get": "list", "put": "update"}),
    ),
    path(
        "profile-data",
        ProfileDataViewSet.as_view({"get": "list", "put": "update"}),
    ),
    path(
        "unregister",
        ProfileUnregisterViewSet.as_view({"delete": "destroy", "put": "update"}),
    ),
    path(
        "finance-details",
        FinanceDetailsViewSet.as_view({"get": "list", "put": "update"}),
    ),
    path("stats", StatsViewSet.as_view({"get": "get_stats"})),
    path("newsletter-subscribe", NewsletterSubscribeViewSet.subscribe),
    path(
        "newsletter-unsubscribe/<str:uuid>",
        NewsletterUnsubscribeViewSet.unsubscribe,
    ),
    path(
        "certificate/<str:id>",
        CertificateViewSet.get_certificate,
    ),
    path("contact", ContactViewSet.as_view({"post": "contact"})),
    path(
        "coupon-validate/<str:coupon_code>/<str:total>",
        CouponValidationViewSet.validate,
    ),
    path("login-google", GoogleLoginViewSet.as_view({"post": "post"})),
    path("login-facebook", FacebookLoginViewSet.as_view({"post": "post"})),
    path("login-github", GithubLoginViewSet.as_view({"post": "post"})),
]

urlpatterns = [
    path(
        "api/",
        include(api_urlpatterns),
    ),
    path("admin", admin.site.urls),
]
