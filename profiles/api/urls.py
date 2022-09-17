from django.urls import path
from .views import (
    ProfileListApiView,
)

urlpatterns=[ 
    path('profile-list/',ProfileListApiView.as_view()),
]