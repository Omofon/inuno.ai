from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    register_view,
    logout_view,
    UserProfileView,
    DeleteUserView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", register_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("delete/", DeleteUserView.as_view(), name="delete_user"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
