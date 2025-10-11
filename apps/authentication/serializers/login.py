# from base.serializers import serializers
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers

from ..models.custom_user import CustomUser

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is not active.")
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError('Must include "email" and "password".')
