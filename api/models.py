from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator

User = get_user_model()


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
