from django.urls import path
from . import views

urlpatterns = [
    # path("api/v1/products/", views.products_list),
    path("api/v1/products/", views.ProductsListAPIView.as_view()),
    path("api/v1/products/info/", views.products_info),
    path("api/v1/products/out-of-stock/", views.ProductListOutOfStockAPIView.as_view()),
    # path("api/v1/product/<int:pk>/", views.product_list),
    path("api/v1/product/<int:product_id>/", views.ProductDetailAPIView.as_view()),
    # path("api/v1/orders/", views.orders_list),
    path("api/v1/orders/", views.OrdersListAPIView.as_view()),
    path(
        "api/v1/user-orders/", views.UserOderListAPIView.as_view(), name="user-orders"
    ),
]
