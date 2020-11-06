from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserRole(models.TextChoices):
    USER = 'US', _('user')
    MODERATOR = 'MD', _('moderator')
    ADMIN = 'AM', _('administrator')


class User(AbstractUser):
    bio = models.CharField(
        max_length=50,
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
