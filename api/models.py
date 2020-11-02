from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator


class Review(models.Model):
#    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name="reviews")
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
    