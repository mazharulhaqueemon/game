from django.urls import path
from .views import (
    CreateTokenView,RegisterWithProfileCreateApiView,LogoutCreateApiView,
    ChangePasswordUpdateApiView,PasswordResetOtpCreateApiView,ResetPasswordUpdateApiView,
    )

urlpatterns=[ 
    path('token/',CreateTokenView.as_view()),
    path('register-with-profile-create/',RegisterWithProfileCreateApiView.as_view()),
    path('logout/',LogoutCreateApiView.as_view()),

    path("change-password/",ChangePasswordUpdateApiView.as_view()),
    path('password-reset-otp-create/',PasswordResetOtpCreateApiView.as_view()),
    path("reset-password/",ResetPasswordUpdateApiView.as_view()),
]