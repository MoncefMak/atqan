from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=None, required=False)
    updated_by = serializers.HiddenField(default=None, required=False)

    class Meta:
        model = User
        fields = ["id", "email", "password", "created_by", "updated_by"]
        extra_kwargs = {'password': {'write_only': True}}


class LogInSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token
