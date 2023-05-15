from typing import Any
from django import forms
# we use get_user_model when we need to call the user abstracted model
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username",
                "email", "password1", "password2"]

    # just to clean email before sending to database
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'class':"form-control", "placeholder": "Username or Email"}),
        )
    
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class":"form-control", "placeholder":"Password"}
                )
            )