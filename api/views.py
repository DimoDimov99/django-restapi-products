# function based view
# from django.http import JsonResponse
from django.db.models import Max
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, OrderItem, Product, User

# from django.shortcuts import get_object_or_404
from api.serializers import (
    OrderItemSerializer,
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
    OrderCreateSerializer,
    UserSerializer,
)

from rest_framework.decorators import action

# @api_view(["GET"])
# def products_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(
#         products, many=True
#     )  # many is true if we want to return a list of objects
#     # return JsonResponse({"data": serializer.data})
#     return Response(serializer.data, status=status.HTTP_200_OK)


# class ProductsListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     # queryset = Product.objects.filter(stock__gt=0)
#     serializer_class = ProductSerializer
#     # permission_classes


# class ProductsCreateAPIView(generics.CreateAPIView):
#     model = Product
#     serializer_class = ProductSerializer

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)


# customizing permissions
class ProductListCreateAPIView(generics.ListCreateAPIView):

    # UnorderedObjectListWarning fix
    # queryset = Product.objects.all() -> queryset = Product.objects.order_by("pk")
    queryset = Product.objects.order_by("pk")
    serializer_class = ProductSerializer
    # filter with URL?=<name>
    # filterset_fields = ("name", "price")
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
    ]
    # You can also perform a related lookup on a ForeignKey or ManyToManyField with the lookup API double-underscore notation
    # profile__profession profile (module) | profession (field)
    # =name -> exact match name only partial match
    search_fields = ["name", "description", "price"]
    ordering_fields = ["name", "price", "stock"]
    # https://www.django-rest-framework.org/api-guide/pagination/#cursorpagination
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    # rename name of paginator
    # pagination_class.page_query_param = "dimo"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 9

    def get_permissions(self):
        # Everyone can get access to all available products
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            # only admin users can create new products
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductListOutOfStockAPIView(generics.ListAPIView):
    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer


# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = "product_id"


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        # Everyone can get access to all available products
        self.permission_classes = [AllowAny]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            # only admin users can create new products
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    # Overwrite the message when product is not found
    # def get_object(self):
    #     try:
    #         return super().get_object()
    #     except Http404:
    #         raise NotFound(detail="The requested item does not exist.")


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


# class OrdersListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items", "items__product")
#     serializer_class = OrderSerializer


# class UserOderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related("items", "items__product")
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         query_set = super().get_queryset()
#         return query_set.filter(user=user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items", "items__product")
    serializer_class = OrderSerializer
    # OrderCreateSerializer on POST
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == "POST"
        if self.action == "create" or self.action == "update":
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # handle unlogged user
    # @action(
    #     detail=False,
    #     methods=["get"],
    #     url_path="user-orders",
    #     # permission_classes=[IsAuthenticated],
    # )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)


# @api_view(["GET"])
# def products_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializer(
#         {
#             "products": products,
#             "count": len(products),
#             "max_price": products.aggregate(max_price=Max("price"))["max_price"],
#         }
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)


class ProductsInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "count": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
