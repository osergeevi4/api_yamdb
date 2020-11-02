from django.db import models


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
    title = models.ForeignKey(Title, blank=False, on_delete=models.CASCADE)
    text = models.TextField(max_length=2500)