from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


from .util_services import _send_email

EMAIL_VERIFICATION_TOKEN_GENERATOR = default_token_generator


def send_letter_for_email_verification(domain: str, user: User) -> None:
    """Sends email to given user for email verification.
       Uses domain to generate verification link"""
    mail_subject = 'Activate your todo app account.'
    template = 'users/email_confirm/confirm_email_letter.html'
    _send_email(domain, user, mail_subject,
                template, EMAIL_VERIFICATION_TOKEN_GENERATOR)


def complete_email_verification(uidb64: str, token: str) -> None:
    """Makes user's account to be active if link is valid else raises corresponding exception.
       If token is not valid raises Value Error"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        raise e
    else:
        if EMAIL_VERIFICATION_TOKEN_GENERATOR.check_token(user, token):
            user.is_active = True
            user.save()
        else:
            raise ValueError
