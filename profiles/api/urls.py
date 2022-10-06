from django.urls import path
from .views import (
    ProfileListApiView,ProfileRetrieveApiView,
    ProfileUpdateApiView,
)

urlpatterns=[ 
    path('profile-list/',ProfileListApiView.as_view()),
    path('profile-retrieve/<int:user_id>/',ProfileRetrieveApiView.as_view()),
    path('self-profile-update/',ProfileUpdateApiView.as_view()),
]