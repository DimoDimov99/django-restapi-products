from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
        )

    def validate_stock_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product_name = serializers.CharField(source="product.name")
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = ("product_name", "product_price", "quantity", "item_subtotal")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="total")
    # user_name = serializers.CharField(source="user.name")

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            "order_id",
            "created_at",
            "user",
            # "user_name",
            "status",
            "items",
            "total_price",
        )


class ProductInfoSerializer(serializers.Serializer):
    # get all products, count of products, max price of available prduct
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
