from rest_framework import serializers
from .models import Title, Category, Genre, Review


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugField()
    name = serializers.CharField()

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year', 'description']



    # def create(self, validated_data):
    #     category_data = validated_data.pop('category')
    #     category = Category.objects.get(id=category_data)
    #     return category

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'text']


