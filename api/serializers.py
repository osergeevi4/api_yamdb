from rest_framework import serializers

from .models import Review, Comments, Title, Category, Genre, User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review

    def validate(self, data):
        author = self.context['request'].user
        title_id = self.context.get('title_id')
        if (Review.objects.filter(author=author, title=title_id).exists()
                and self.context['request'].method != 'PATCH'):
            raise serializers.ValidationError('Ваш отзыв уже есть')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'role',
            'email',
            'first_name',
            'last_name',
            'bio',
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=30)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'category',
                  'genre',
                  'year',
                  'description',
                  'rating',)
