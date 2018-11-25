from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Blog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('header', 'content', 'cover', 'markdownContent', 'time', 'readTimes')
