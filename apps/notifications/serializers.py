from rest_framework import serializers

from apps.stock.serializers import StockListSerializer, StockRetrieveSerializer

from .models import Notification, UserNotification


class UserNotificationListSerializer(serializers.ModelSerializer):
    # stock = StockListSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
        # exclude = [
        #     "user",
        #     "stock",
        # ]


class UserNotificationRetrieveSerializer(serializers.ModelSerializer):
    # stock = StockListSerializer()

    class Meta:
        model = Notification
        # fields = "__all__"
        exclude = [
            "user",
            "stock",
        ]


class SystemNotificationSerializer(serializers.ModelSerializer):
    # stock = StockListSerializer()

    class Meta:
        model = Notification
        # fields = "__all__"
        exclude = [
            # "user",
            "stock",
        ]


class SystemNotificationRetrieveSerializer(serializers.ModelSerializer):
    # stock = StockListSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
        # exclude = [
        # "user",
        # "stock",
        # ]


class SignalNotificationSerializer(serializers.ModelSerializer):
    notification = UserNotificationListSerializer()

    class Meta:
        model = UserNotification
        fields = "__all__"
