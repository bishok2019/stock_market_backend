from rest_framework import serializers

from ..models import HistoricalPrice, Stock

# class WatchlistFetchSerializer(serializers.ModelSerializer):
#     stock = serializers.CharField(source="stock.name")
#     symbol = serializers.CharField(source="stock.symbol")
#     price = serializers.CharField(source="stock.price")
#     last_updated = serializers.DateTimeField(source="stock.last_updated")

#     class Meta:
#         model = Watchlist
#         fields = [
#             "stock",
#             "symbol",
#             "price",
#             "last_updated",
#         ]


class HistoricalPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPrice
        fields = "__all__"
