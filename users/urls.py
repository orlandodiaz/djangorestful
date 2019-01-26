from users.views import RegisterView
from django.urls import path
from .views import (
    HelloWorldView,
    LogoutView,
    UserDetailView,
    UserUpdateView,
    PasswordResetView,
    PasswordResetRequestView,
    VerifyPasswordResetTokenView,
    RequestVerifyEmailView,
    VerifyEmailView,
)


urlpatterns = [
    path("create/", RegisterView.as_view(), name="register"),
    path("helloworld", HelloWorldView.as_view(), name="hello-world"),
    path("", UserDetailView.as_view(), name="user-detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit/", UserUpdateView.as_view(), name="user-update"),
    path("verify_email/", VerifyEmailView.as_view(), name="verify-email"),
    path(
        "request_email_verification_email/",
        RequestVerifyEmailView.as_view(),
        name="request-verification-email",
    ),
    path(
        "verify_password_reset_token/", VerifyPasswordResetTokenView.as_view()
    ),
    path(
        "password_reset_request/",
        PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password_reset/<token>",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
]
