from rest_framework import serializers
from .models import Order, OrderItem
from menu.models import Product
from tables.models import Table


class OrderItemInputSerializer(serializers.Serializer):
    """Accepts product ID + quantity for order creation."""
    product = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    """
    Accepts the payload from the frontend:
    {
        "tableNumber": "5",
        "items": [{"product": "1", "quantity": 2}],
        "specialInstructions": "No onions",
        "total": 360
    }
    """
    tableNumber = serializers.CharField()
    items = OrderItemInputSerializer(many=True)
    specialInstructions = serializers.CharField(required=False, allow_blank=True, default='')
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        table_number = validated_data['tableNumber']
        items_data = validated_data['items']
        special_instructions = validated_data.get('specialInstructions', '')

        # Look up or create the table
        table, _ = Table.objects.get_or_create(
            table_number=int(table_number),
            defaults={'qr_code': f'/table/{table_number}'},
        )

        # Calculate total from items
        total_price = 0
        order_items = []
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product'])
            item_total = product.price * item_data['quantity']
            total_price += item_total
            order_items.append(
                OrderItem(
                    product=product,
                    quantity=item_data['quantity'],
                    price=item_total,
                )
            )

        # Create the order
        order = Order.objects.create(
            table=table,
            total_price=total_price,
            status='received',
            special_instructions=special_instructions,
        )

        # Bulk create order items
        for oi in order_items:
            oi.order = order
        OrderItem.objects.bulk_create(order_items)

        return order


class OrderResponseSerializer(serializers.ModelSerializer):
    """Serializes the response after placing an order."""
    id = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Order
        fields = ['id', 'status', 'createdAt']

    def get_id(self, obj):
        return f'ORD{obj.id}'


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
