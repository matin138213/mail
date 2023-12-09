from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'picture']
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data['username']
        password = data['password']

        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError('Username does not exist')
        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid password')

        return data
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

