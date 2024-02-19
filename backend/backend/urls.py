from profile.register.views import ProfileRegisterViewSet
from profile.verify.views import ProfileVerificationCodeViewSet, ProfileVerifyViewSet
from profile.login.views import ProfileLoginViewSet
from profile.logout.views import ProfileLogoutViewSet
from profile.password_change.views import ProfilePasswordChangeViewSet
from profile.password_reset.views import ProfilePasswordResetViewSet
from profile.details.views import ProfileDetailsViewSet
from profile.lecturers.views import LecturerViewSet, BestLecturerViewSet
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from course.views import (
    CourseViewSet,
    BestCourseViewSet,
)
from lesson.views import (
    LessonViewSet,
    LessonPriceHistoryViewSet,

)
from technology.views import TechnologyViewSet
from review.views import ReviewViewSet, ReviewStatsViewSet, BestReviewViewSet
from newsletter.views import (
    NewsletterEntriesViewSet,
    NewsletterSubscribeViewSet,
    NewsletterUnsubscribeViewSet,
)
from schedule.views import ScheduleViewSet
from stats.views import StatsViewSet
from wishlist.views import WishlistViewSet
from cart.views import CartViewSet
from purchase.views import PurchaseViewSet
from teaching.views import TeachingViewSet
from reservation.views import ReservationViewSet
from csrf.views import CsrfViewSet
from contact.views import ContactViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r"register", ProfileRegisterViewSet, basename="user_register")
router.register(r"verify", ProfileVerifyViewSet, basename="user_verification")
router.register(r"login", ProfileLoginViewSet, basename="user_login")
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
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(
    r"lesson-price-history", LessonPriceHistoryViewSet, basename="lesson_price_history"
)
router.register(r"technologies", TechnologyViewSet, basename="technologies")
router.register(r"best-lecturers", BestLecturerViewSet, basename="best_lecturers")
router.register(r"lecturers", LecturerViewSet, basename="lecturers")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"reviews-stats", ReviewStatsViewSet, basename="reviews-stats")
router.register(r"best-reviews", BestReviewViewSet, basename="best_reviews")
router.register(r"schedules", ScheduleViewSet, basename="schedules")
router.register(r"newsletter", NewsletterEntriesViewSet, basename="newsletter")
router.register(
    r"newsletter-subscribe", NewsletterSubscribeViewSet, basename="newsletter_subscribe"
)
router.register(r"wishlist", WishlistViewSet, basename="wishlist")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"purchase", PurchaseViewSet, basename="purchase")
router.register(r"teaching", TeachingViewSet, basename="teaching")
router.register(r"reservation", ReservationViewSet, basename="reservation")


urlpatterns = [
    path("", include(router.urls)),
    path("admin", admin.site.urls),
    path("details", ProfileDetailsViewSet.as_view({"get": "list", "put": "update"})),
    path("stats", StatsViewSet.as_view({"get": "get_stats"})),
    path("csrf", CsrfViewSet.as_view({"get": "get_csrf"})),
    path("newsletter-unsubscribe/<str:uuid>", NewsletterUnsubscribeViewSet.unsubscribe),
    path("contact", ContactViewSet.as_view({"post": "contact"})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
