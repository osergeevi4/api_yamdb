from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'U'
    MODERATOR = 'M'
    ADMINISTRATOR = 'A'
    ROLE_CHOISES = (
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMINISTRATOR, 'Administrator')
    )
    bio = models.CharField(max_length=50, blank=True)
    role = models.CharField(
        max_length=1,
        choices=ROLE_CHOISES,
        default=USER,
    )
    REQUIRED_FIELDS = ['email']


class Auth(models.Model):
    email = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    confirmation_code = models.CharField(max_length=20)

