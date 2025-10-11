from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...authentication.models import UserProfile
from ..models import HistoricalPrice, Stock
from ..serializers import HistoricalPriceSerializer, StockListSerializer


class WatchlistAddOrRemoveApiView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        stock_id = kwargs.get("stock_id")
        try:
            stock = Stock.objects.get(pk=stock_id)
        except Stock.DoesNotExist:
            return Response(
                {"message": "Stock does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if stock in user_profile.watchlisted_stock.all():
            user_profile.watchlisted_stock.remove(stock)
            action = "removed"
        else:
            user_profile.watchlisted_stock.add(stock)
            action = "added"

        return Response(
            {"message": f"Stock {action} successfully."},
            status=status.HTTP_200_OK,
        )


class WatchListApiView(generics.ListAPIView):
    serializer_class = StockListSerializer

    def get_queryset(self):
        request = self.request
        if request.user.is_authenticated:
            try:
                return self.request.user.profile.watchlisted_stock.all()
            except Exception:
                pass
        return Stock.objects.none()


class HistoricalPriceApiView(generics.ListAPIView):
    serializer_class = HistoricalPriceSerializer

    def get_queryset(self):
        stock_id = self.kwargs.get("stock_id")
        return HistoricalPrice.objects.filter(stock_id=stock_id)
