from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from .util_services import _send_email

PASSWORD_RESET_TOKEN_GENERATOR = default_token_generator


def get_user_by_email(email: str) -> User:
    """Returns user with given email or raises Does Not Exist Error"""

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist as e:
        raise e
    else:
        return user


def send_letter_for_password_reset(domain: str, user: User) -> None:
    """Sends email to given user for password reset.
       Uses domain to generate reset link"""

    mail_subject = 'ToDo app password reset'
    template = 'users/password_reset/reset_password_letter.html'
    _send_email(domain, user, mail_subject,
                template, PASSWORD_RESET_TOKEN_GENERATOR)
