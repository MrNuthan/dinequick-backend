from django.urls import path
from .views import PlaceOrderView, OrderStatusView

urlpatterns = [
    path('', PlaceOrderView.as_view(), name='place-order'),
    path('<str:order_id>/status/', OrderStatusView.as_view(), name='order-status'),
]
