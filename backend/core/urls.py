from profile.users.views import UserViewSet
from profile.register.views import ProfileRegisterViewSet
from profile.unregister.views import ProfileUnregisterViewSet
from profile.verify.views import ProfileVerificationCodeViewSet, ProfileVerifyViewSet
from profile.login.views import (
    EmailLoginViewSet,
    GoogleLoginAPIView,
    FacebookLoginAPIView,
    GithubLoginAPIView,
)
from profile.logout.views import ProfileLogoutViewSet
from profile.password_change.views import ProfilePasswordChangeViewSet
from profile.password_reset.views import ProfilePasswordResetViewSet
from profile.personal_data.views import PersonalDataViewSet
from profile.profile_data.views import ProfileDataViewSet
from profile.lecturers.views import LecturerViewSet, BestLecturerViewSet
from profile.earnings.views import EarningViewSet
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
import debug_toolbar
from course.views import (
    CourseViewSet,
    BestCourseViewSet,
)
from notification.views import NotificationViewSet
from message.views import MessageViewSet
from certificate.views import CertificateViewSet, CertificateInfoAPIView
from lesson.views import (
    LessonViewSet,
    LessonPriceHistoryViewSet,
)
from module.views import ModuleViewSet
from technology.views import TechnologyViewSet, BestTechnologyViewSet
from topic.views import TopicViewSet
from candidate.views import CandidateViewSet
from tag.views import TagViewSet
from post.views import PostViewSet, PostCategoryViewSet
from review.views import ReviewViewSet, ReviewStatsViewSet, BestReviewViewSet
from newsletter.views import (
    NewsletterEntriesViewSet,
    NewsletterSubscribeAPIView,
    NewsletterUnsubscribeAPIView,
)
from schedule.views import (
    ManageScheduleViewSet,
    ScheduleViewSet,
    ScheduleAvailableDateViewSet,
)
from stats.views import StatsAPIView
from wishlist.views import WishlistViewSet
from cart.views import CartViewSet
from purchase.views import (
    PurchaseViewSet,
    PaymentViewSet,
    PaymentVerifyAPIView,
    PaymentStatusViewSet,
)
from teaching.views import ManageTeachingViewSet, TeachingViewSet
from reservation.views import ReservationViewSet
from contact.views import ContactAPIView
from finance.views import FinanceDetailsViewSet, FinanceHistoryViewSet
from coupon.views import CouponViewSet, CouponUserViewSet, CouponValidationAPIView
from .routers import Router

router = Router(trailing_slash=False)

router.register(r"best-courses", BestCourseViewSet, basename="best_courses")
router.register(r"best-lecturers", BestLecturerViewSet, basename="best_lecturers")
router.register(r"best-reviews", BestReviewViewSet, basename="best_reviews")
router.register(
    r"best-technologies", BestTechnologyViewSet, basename="best_technologies"
)
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"certificates", CertificateViewSet, basename="certificates")
router.register(r"coupons", CouponViewSet, basename="coupons")
router.register(r"coupon-usage", CouponUserViewSet, basename="coupon_usage")
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"earnings", EarningViewSet, basename="earnings")
router.register(r"finance-history", FinanceHistoryViewSet, basename="finance_history")
router.register(r"lessons", LessonViewSet, basename="lessons")
router.register(
    r"lesson-dates", ScheduleAvailableDateViewSet, basename="lesson_schedules_dates"
)
router.register(r"lesson-lecturers", TeachingViewSet, basename="lesson_lecturers")
router.register(
    r"lesson-price-history", LessonPriceHistoryViewSet, basename="lesson_price_history"
)
router.register(r"lesson-schedules", ScheduleViewSet, basename="lesson_schedules")
router.register(r"lecturers", LecturerViewSet, basename="lecturers")
router.register(r"login", EmailLoginViewSet, basename="user_login")
router.register(r"logout", ProfileLogoutViewSet, basename="user_logout")
router.register(r"messages", MessageViewSet, basename="messages")
router.register(r"modules", ModuleViewSet, basename="modules")
router.register(r"newsletter", NewsletterEntriesViewSet, basename="newsletter")
router.register(r"notifications", NotificationViewSet, basename="notifications")
router.register(
    r"password-change", ProfilePasswordChangeViewSet, basename="user_password_change"
)
router.register(
    r"password-reset", ProfilePasswordResetViewSet, basename="user_password_reset"
)
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"post-categories", PostCategoryViewSet, basename="post_categories")
router.register(r"purchase", PurchaseViewSet, basename="purchase")
router.register(r"payments", PaymentViewSet, basename="payments")
router.register(r"register", ProfileRegisterViewSet, basename="user_register")
router.register(r"reservation", ReservationViewSet, basename="reservation")
router.register(r"reviews", ReviewViewSet, basename="reviews")
router.register(r"reviews-stats", ReviewStatsViewSet, basename="reviews-stats")
router.register(r"schedules", ManageScheduleViewSet, basename="schedules")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"teaching", ManageTeachingViewSet, basename="teaching")
router.register(r"technologies", TechnologyViewSet, basename="technologies")
router.register(r"topics", TopicViewSet, basename="topics")
router.register(r"candidates", CandidateViewSet, basename="candidates")
router.register(r"users", UserViewSet, basename="users")
router.register(r"verify", ProfileVerifyViewSet, basename="user_verification")
router.register(
    r"verify-code", ProfileVerificationCodeViewSet, basename="user_verification_code"
)
router.register(r"wishlist", WishlistViewSet, basename="wishlist")


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
    path("stats", StatsAPIView.as_view()),
    path("newsletter-subscribe", NewsletterSubscribeAPIView.as_view()),
    path(
        "newsletter-unsubscribe/<str:uuid>",
        NewsletterUnsubscribeAPIView.as_view(),
    ),
    path(
        "certificate/<str:id>",
        CertificateInfoAPIView.as_view(),
    ),
    path(
        "payment-verify",
        PaymentVerifyAPIView.as_view(),
    ),
    path(
        "payment-status",
        PaymentStatusViewSet.as_view({"get": "list"}),
    ),
    path("contact", ContactAPIView.as_view()),
    path(
        "coupon-validate/<str:coupon_code>/<str:total>",
        CouponValidationAPIView.as_view(),
    ),
    path("login-google", GoogleLoginAPIView.as_view()),
    path("login-facebook", FacebookLoginAPIView.as_view()),
    path("login-github", GithubLoginAPIView.as_view()),
]

urlpatterns = [
    path(
        "api/",
        include(api_urlpatterns),
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]  # pragma: no cover

    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )  # pragma: no cover
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # pragma: no cover
