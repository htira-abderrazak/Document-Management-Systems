from django.urls import path,include
from rest_framework.authtoken import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views as view

urlpatterns=[
    path('register/',view.RegisterUserAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',view.LogoutView.as_view(),name='logoutView')
]