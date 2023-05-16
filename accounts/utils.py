from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages
from .tokens import account_activation_token
from .models import CustomUser

# see if you can do anything here
# from .decorators import user_not_authenticated

def activateEmail(request, user: CustomUser, to_email: str):
    """
    Summary:
    activateEmail function takes three parameters: request, user, and recieving email

    Args:
        1] request (HttpReuqest): the request\n
        2] user (AbstractUser): inactive user\n
        3] to_email (str): recieving account
    """
    
    mail_subject = f"{user.first_name} Activate Your Account"
    message = render_to_string("template_activate_account.html", {
        "user": user.username, 
        "protocol": "https" if request.is_secure() else "http",
        # get current site, if the SITE_ID setting isn't defined it return 127.0.0.1
        "domain": get_current_site(request).domain,
        # Encode a bytestring to a base64 string for use in URLs, Strip any trailing equal signs
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": account_activation_token.make_token(user),
    })
    
    # from here the activation email is sent
    email = EmailMessage(mail_subject, message, to=[to_email])
    
    if email.send():
        messages.success(request, f"{user.username}please go to your email {to_email} click on recieved activation link to \
            confirm and complete the registration. \
            Note: Check your spam.")
    else:
        messages.error(request, f"problem sending email to {to_email}, try again later.")