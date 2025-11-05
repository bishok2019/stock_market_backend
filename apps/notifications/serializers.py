from rest_framework import serializers

from apps.stock.serializers import StockListSerializer, StockRetrieveSerializer

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    stock = StockListSerializer()

    class Meta:
        model = Notification
        fields = "__all__"
