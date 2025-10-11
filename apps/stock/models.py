from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    last_updated = models.DateTimeField(auto_now=True)

    # Historical data tracking
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"


class HistoricalPrice(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="historical_prices"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol} - {self.price} at {self.timestamp}"
