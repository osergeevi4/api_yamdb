from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth import get_user_model

from .models import Title, Category, Genre, Review
from .serializer import (TitleSerializer, CategorySerializer, GenreSerializer,)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Title.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer

    def get_queryset(self):
        return Genre.objects.all()
