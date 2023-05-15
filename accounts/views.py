from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import (
    login, logout, authenticate
    )
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterationForm, UserLoginForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
# from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

# Create your views here.

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect(reverse('accounts:login'))
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect(reverse("home"))


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):
    form = UserRegisterationForm()
    context = {
        "form": form
    }
    if request.method == "POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            # save without going to database 
            user = form.save(commit=False)
            # deactivate user before activation email
            user.is_active = False
            # after deactivating user we commit to database
            user.save()
            # now we have user but notactivated, so we have to activate it via email activation
            activateEmail(request, user, form.cleaned_data.get("email"))
            # login(request, user)
            # messages.success(request, f"{user.first_name}, your account has been created")
            return redirect(reverse("home"))
        else:
            for message in list(form.errors.values()):
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
            # scanning username ond password in the database
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # if they are in the database
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
