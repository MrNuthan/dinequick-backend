from django.db import models
from orders.models import Order


class Payment(models.Model):
    """Razorpay payment record."""

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment',
    )
    razorpay_order_id = models.CharField(max_length=100, blank=True, default='')
    razorpay_payment_id = models.CharField(max_length=100, blank=True, default='')
    razorpay_signature = models.CharField(max_length=200, blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for ORD{self.order_id} — {self.status}'
