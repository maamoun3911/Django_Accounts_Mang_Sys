from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserRegisterationForm, UserLoginForm
    )
from django.contrib.auth import (
    login, logout, authenticate
    )
from .utils import activateEmail 
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

# new
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


def activate(request, uidb64, token):
    # maybe we can comment this line
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect(reverse('accounts:login'))
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect(reverse("home"))


def register(request):
    form = UserRegisterationForm()
    context = {
        "form": form
    }
    if request.method =="POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            # save without going to database
            user = form.save(commit=False)
            user.is_active = False
            # after deactivating user we commit to database
            user.save()
            # now we have inactivated user, so we have to activate it via activateEmail function
            activateEmail(request, user, user.email)
            return redirect(reverse("home"))
        else:
            for message in form.errors.values():
                messages.error(request, message)
                
    return render(request,"Create_Account.html", context)


def login_view(request):
    form = UserLoginForm()
    context = {
        "form":form
    }
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        # if the form achieve email and password recognized principles
        if form.is_valid():
            # scanning username ond password in the database through new backend code
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # if user in the database
            if user:
                login(request, user)
                messages.success(request, f"{user.username} Logged in Successfully")
                return redirect(reverse("home"))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    return render(request, "login.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged Out Succesfully")
    return redirect(reverse("home"))
