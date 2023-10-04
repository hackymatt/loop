from profile.register.views import ProfileRegisterViewSet
from profile.verify.views import ProfileVerificationCodeViewSet, ProfileVerifyViewSet
from profile.login.views import ProfileLoginViewSet
from profile.logout.views import ProfileLogoutViewSet
from profile.password_change.views import ProfilePasswordChangeViewSet
from profile.password_reset.views import ProfilePasswordResetViewSet
from profile.details.views import ProfileDetailsViewSet
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

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

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
    path("admin", admin.site.urls),
    path("details", ProfileDetailsViewSet.as_view({"get": "list", "put": "update"})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
