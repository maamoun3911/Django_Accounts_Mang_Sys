from django.urls import path
from .views import (
    register, login_view, logout_view, activate
    )

app_name = "accounts"

urlpatterns = [
    path("Register/", register, name="register"),
    path("Login/", login_view, name="login"),
    path("Logout/", logout_view, name="logout"),
    path('activate/<uidb64>/<token>', activate, name='activate')
]
