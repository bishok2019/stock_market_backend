from django.urls import include, path

from .views import (
    HistoricalPriceApiView,
    StockCreateApiView,
    StockListView,
    StockRetrieveApiView,
    StockUpdateApiView,
    WatchlistAddOrRemoveApiView,
    WatchListApiView,
)

stock_patterns = [
    path("create", StockCreateApiView.as_view(), name="list-stock"),
    path("list", StockListView.as_view(), name="list-stock"),
    path("retrieve/<int:pk>", StockRetrieveApiView.as_view(), name="retrieve-stock"),
    path("update/<int:pk>", StockUpdateApiView.as_view(), name="update-stock"),
]

watchlist_patterns = [
    path("list", WatchListApiView.as_view(), name="list-watchlist"),
    path(
        "add-or-remove/<int:stock_id>",
        WatchlistAddOrRemoveApiView.as_view(),
        name="add-or-remove-watchlist",
    ),
]

urlpatterns = [
    path("stock/", include(stock_patterns)),
    path("watchlist/", include(watchlist_patterns)),
    path(
        "historical_price/<int:stock_id>",
        HistoricalPriceApiView.as_view(),
        name="hitory",
    ),
]
