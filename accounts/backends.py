# Don't Forget to Edit AUTHENTICATION_BACKEND in settings to the new Backend inheritanced class

from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.db.models import Q

User = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str | None = None, password: str | None = None, **kwargs: Any) -> AbstractUser | None:
        # we write something and try to find it as email or username col so Q is the convenient choice
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        # if the (username | email) isn't exist then we retrn nothing
        except User.DoesNotExist:
            User.set_password(password)
            return
        # if there's many choices, then pick first one
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by("id").first
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user