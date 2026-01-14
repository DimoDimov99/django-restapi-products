# function based view
# from django.http import JsonResponse
from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view


# @api_view(["GET"])
# def products_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(
#         products, many=True
#     )  # many is true if we want to return a list of objects
#     # return JsonResponse({"data": serializer.data})
#     return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    # permission_classes


class ProductListOutOfStockAPIView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"


# @api_view(["GET"])
# def product_list(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(
#         product
#     )  # many is true if we want to return a list of objects
#     # return JsonResponse({"data": serializer.data})
#     return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# def orders_list(request):
#     # orders = Order.objects.all()
#     # optimization
#     # items is no longer needed, due to items__product
#     # .all() not needed due to prefetch_related()
#     orders = Order.objects.prefetch_related("items", "items__product")
#     serializer = OrderSerializer(
#         orders, many=True
#     )  # many is true if we want to return a list of objects
#     # return JsonResponse({"data": serializer.data})
#     return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product")
    serializer_class = OrderSerializer


class UserOderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        query_set = super().get_queryset()
        return query_set.filter(user=user)


@api_view(["GET"])
def products_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "count": len(products),
            "max_price": products.aggregate(max_price=Max("price"))["max_price"],
        }
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
