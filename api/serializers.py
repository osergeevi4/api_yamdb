from rest_framework import serializers
from .models import User, Auth


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auth
        fields = '__all__'
