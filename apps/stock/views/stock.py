from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from ..models import Stock
from ..serializers import (
    StockCreateSerializer,
    StockListSerializer,
    StockRetrieveSerializer,
    StockUpdateSerializer,
)


class StockListView(generics.ListAPIView):
    serializer_class = StockListSerializer
    permission_classes = [AllowAny]
    queryset = Stock.objects.all()


class StockCreateApiView(generics.CreateAPIView):
    serializer_class = StockCreateSerializer
    permission_classes = [IsAdminUser]


class StockRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = StockRetrieveSerializer
    permission_classes = []
    queryset = Stock.objects.all()


class StockUpdateApiView(generics.UpdateAPIView):
    serializer_class = StockUpdateSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["patch"]
    queryset = Stock.objects.all()
