from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "description",
            "name",
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


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ("product", "quantity")

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def create(self, validated_data):
        # pops out the items out of the validated_data
        order_item_data = validated_data.pop("items")
        with transaction.atomic():
            # order do not need order_items, they can be created later
            order = Order.objects.create(**validated_data)

            for item in order_item_data:
                OrderItem.objects.create(order=order, **item)

        return order

    def update(sefl, instance, validated_data):
        order_item_data = validated_data.pop("items")

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if order_item_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all.delete()

                # Recreate items with the update data

                for item in order_item_data:
                    OrderItem.object.create(order=instance, **item)

            return instance

    class Meta:
        model = Order
        fields = (
            "order_id",
            "user",
            # "user_name",
            "status",
            "items",
        )
        extra_kwargs = {"user": {"read_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    # automatically generate uuid for order_id
    order_id = serializers.UUIDField(read_only=True)
    # writable nested representations restapi wiki
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
