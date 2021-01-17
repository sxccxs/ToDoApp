from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.contrib.auth.models import User


def _send_email(domain: str, user: User, mail_subject: str, letter_template: str,
                token_generator: PasswordResetTokenGenerator = default_token_generator) -> None:
    """Generates token for given user and sends email with given parameters"""
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user)
    }
    message = render_to_string(letter_template, context)
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
