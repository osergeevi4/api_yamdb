from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    bio = models.CharField(max_length=50, blank=True)
    role = models.CharField(
        max_length=10,
        choices=UserRole,
        default=UserRole.USER,
    )
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
