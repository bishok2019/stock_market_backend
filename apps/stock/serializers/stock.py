from rest_framework import serializers

from ..models import HistoricalPrice, Stock


class StockCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        stock = Stock.objects.create(**validated_data)
        HistoricalPrice.objects.create(stock=stock, price=stock.price)
        return stock


class StockListSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()
    initial_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = ["id", "symbol", "name", "initial_price", "latest_price"]

    def get_latest_price(self, obj):
        latest = obj.historical_prices.order_by("-timestamp").first()
        return latest.price if latest else None

    def get_initial_price(self, obj):
        initial = obj.historical_prices.order_by("timestamp").first()
        return initial.price if initial else None


class StockRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class StockUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

    def update(self, instance, validated_data):
        old_price = instance.price
        stock = super().update(instance, validated_data)

        # if existing price changes, create histry
        if old_price != stock.price:
            HistoricalPrice.objects.create(stock=stock, price=stock.price)
        return stock
