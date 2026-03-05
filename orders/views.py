from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order
from .serializers import OrderCreateSerializer, OrderResponseSerializer, OrderStatusSerializer


class PlaceOrderView(APIView):
    """POST /api/orders/ — place a new order."""

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response_serializer = OrderResponseSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusView(APIView):
    """GET /api/orders/{order_id}/status/ — get current order status."""

    def get(self, request, order_id):
        # Support both raw integer ID and "ORD123" format
        clean_id = order_id.replace('ORD', '').replace('ord', '')
        try:
            order = Order.objects.get(id=clean_id)
        except (Order.DoesNotExist, ValueError):
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OrderStatusSerializer(order)
        return Response(serializer.data)
