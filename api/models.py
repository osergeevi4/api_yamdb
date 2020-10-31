from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOISES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    bio = models.CharField(max_length=50, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOISES,
        default=USER,
    )
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']


