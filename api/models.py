from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.CharField(max_length=50, blank=False, null=True, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    slug = models.CharField(max_length=50, blank=False, null=True, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, blank=False, null=True, on_delete=models.SET_NULL)
    year = models.IntegerField(blank=False, null=True)
    description = models.TextField(max_length=500, blank=False, null=True)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10, message="Поставьте оценку от 1 до 10")])
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    pub_date = models.DateTimeField("Дата добавления отзыва", auto_now_add=True, db_index=True)


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления комментария", auto_now_add=True, db_index=True)
    
# Олех
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

