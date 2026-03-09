
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from .models import Payment
from .serializers import CreateRazorpayOrderSerializer, VerifyPaymentSerializer


def get_razorpay_client():
    """Lazily create Razorpay client from env variables."""
    import razorpay
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateRazorpayOrderView(APIView):
    """
    POST /api/payments/create-order/
    Creates a Razorpay order for the given internal order.
    """

    def post(self, request):
        serializer = CreateRazorpayOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Amount in paise (INR smallest unit)
        amount_paise = int(order.total_amount * 100)

        client = get_razorpay_client()
        razorpay_order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'ORD{order.id}',
        })

        # Create or update Payment record
        payment, _ = Payment.objects.update_or_create(
            order=order,
            defaults={
                'razorpay_order_id': razorpay_order['id'],
                'amount': order.total_amount,
                'status': 'created',
            },
        )

        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_paise,
        })


class VerifyPaymentView(APIView):
    """
    POST /api/payments/verify/
    Verifies Razorpay payment signature and marks the order as completed.
    """

    def post(self, request):
        import razorpay

        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        razorpay_order_id = serializer.validated_data['razorpay_order_id']
        razorpay_payment_id = serializer.validated_data['razorpay_payment_id']
        razorpay_signature = serializer.validated_data['razorpay_signature']

        client = get_razorpay_client()

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })
        except razorpay.errors.SignatureVerificationError:
            # Mark payment as failed
            Payment.objects.filter(
                razorpay_order_id=razorpay_order_id,
            ).update(status='failed')
            return Response(
                {'error': 'Payment verification failed'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Signature valid — update Payment record
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment record not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'successful'
        payment.save()

        # Mark the associated order as completed
        order = payment.order
        order.status = 'completed'
        order.save()

        return Response({'status': 'Payment verified successfully'})