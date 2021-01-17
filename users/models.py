from django.contrib.auth.models import User


User._meta.get_field('email')._unique = True  # Makes Django UserModel's field email to be unique
