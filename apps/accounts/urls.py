from django.urls import path
from .views import (JwtLoginView,
    JwtRefreshView,LoginView, LogoutView, MeView, RegisterView, UserListView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("me/", MeView.as_view(), name="me"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("jwt/login/", JwtLoginView.as_view(), name="jwt-login"),
    path("jwt/refresh/", JwtRefreshView.as_view(), name="jwt-refresh"),
]