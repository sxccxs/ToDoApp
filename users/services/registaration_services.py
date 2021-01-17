from django.contrib.auth.models import User
from ..forms import CreateUserForm


def create_non_active_user_from_form(form: CreateUserForm) -> User:
    """Creates user from given form, sets field is_active to be False
       and saves it"""
    user = form.save(commit=False)
    user.is_active = False
    user.save()
    return user
