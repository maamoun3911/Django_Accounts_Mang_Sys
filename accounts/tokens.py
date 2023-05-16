from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # 1. The password field will change upon a password reset (even if the
    #   same password is chosen, due to password salting).
    # 2. The last_login field will usually be updated very shortly after
    #   a password reset.
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

# we make object here so we send and recieve same token object (important for validation)
account_activation_token = AccountActivationTokenGenerator()