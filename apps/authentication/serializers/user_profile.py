from rest_framework import serializers

from ..models import UserProfile


class UserProfileGetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username")

    class Meta:
        model = UserProfile
        fields = ["name", "watchlisted_stock", "stock"]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


# class UserProfileGetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = "__all__"
