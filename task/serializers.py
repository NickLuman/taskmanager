from rest_framework import serializers 
from rest_framework.authtoken.models import Token

from .models import Task, TaskChange
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'created',
            'status',
            'completion',
        )


class TaskChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskChange
        fields = (
            'id',
            'changed_title',
            'changed_description',
            'changed_status',
            'changed_completion',
            'changed_at',
        )
