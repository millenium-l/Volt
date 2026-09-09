from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from voltvibe.models import Order

from .mpesa import initiate_stk_push
from .models import Payment


def normalize_phone(phone_number):
    phone_number = phone_number.replace(' ', '').replace('-', '')
    if phone_number.startswith('07') or phone_number.startswith('01'):
        return f'254{phone_number[1:]}'
    if phone_number.startswith('+254'):
        return phone_number[1:]
    return phone_number


@login_required
@require_http_methods(['GET'])
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user, complete=False)
    return render(request, 'payments/payment.html', {'order': order, 'total': round(order.get_cart_total)})


@login_required
@require_POST
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user, complete=False)
    details = request.session.pop('payment_details', {})
    name = details.get('name')
    phone_number = details.get('phone_number')

    if not name or not phone_number:
        return JsonResponse({'error': 'Checkout details are missing.'}, status=400)

    phone_number = normalize_phone(phone_number)
    payment = Payment.objects.create(
        order=order,
        customer_name=name,
        phone_number=phone_number,
        amount=round(order.get_cart_total),
    )

    try:
        result = initiate_stk_push(
            phone_number,
            payment.amount,
            f'ORDER-{order.id}',
            f'VoltVibe order {order.id}',
        )
    except Exception as error:
        payment.status = Payment.STATUS_FAILED
        payment.result_description = str(error)
        payment.save(update_fields=['status', 'result_description', 'updated_at'])
        return JsonResponse({'error': 'Unable to start M-Pesa payment.'}, status=502)

    payment.merchant_request_id = result.get('MerchantRequestID', '')
    payment.checkout_request_id = result.get('CheckoutRequestID', '')
    payment.result_description = result.get('ResponseDescription', '')
    payment.save(update_fields=[
        'merchant_request_id', 'checkout_request_id', 'result_description', 'updated_at',
    ])
    return JsonResponse({'message': result.get('CustomerMessage', 'Check your phone to complete payment.')})


@csrf_exempt
@require_POST
def mpesa_callback(request):
    try:
        payload = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid JSON'}, status=400)
    callback = payload.get('Body', {}).get('stkCallback', {})
    checkout_request_id = callback.get('CheckoutRequestID')
    payment = Payment.objects.filter(checkout_request_id=checkout_request_id).first()

    if payment:
        payment.callback_payload = payload
        payment.result_description = callback.get('ResultDesc', '')
        if callback.get('ResultCode') == 0:
            payment.status = Payment.STATUS_SUCCESS
            metadata = callback.get('CallbackMetadata', {}).get('Item', [])
            receipt = next((item.get('Value') for item in metadata if item.get('Name') == 'MpesaReceiptNumber'), '')
            payment.receipt_number = str(receipt)
            payment.order.transaction_id = payment.receipt_number
            payment.order.complete = True
            payment.order.save(update_fields=['transaction_id', 'complete'])
        else:
            payment.status = Payment.STATUS_FAILED
        payment.save()

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})