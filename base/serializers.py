from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ActionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
