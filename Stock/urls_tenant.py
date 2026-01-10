from django.urls import path, include


urlpatterns = [
    path("api/stock/", include("stock_management.urls")),
]
