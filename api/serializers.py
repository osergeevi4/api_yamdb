from rest_framework import serializers
from .models import User
from .models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH' and
            Review.objects.filter(title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError('Score already exists')
        return data

    class Meta:
        exclude = ['title']
        model = Review
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        exclude = ['review']
        model = Comments

# Олег
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

