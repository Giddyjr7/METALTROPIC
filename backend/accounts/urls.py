from django.urls import path
from .views import index, RegisterView, ProfileView, ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView

urlpatterns = [
    path("", index, name="accounts_index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("reset-password/", ResetPasswordRequestView.as_view(), name="reset-password"),
    path("reset-password-confirm/", ResetPasswordConfirmView.as_view(), name="reset-password-confirm"),
]
