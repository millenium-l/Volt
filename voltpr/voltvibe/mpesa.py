import base64
import hashlib
import hmac
from datetime import datetime
from decimal import Decimal

import requests
from django.conf import settings


def normalize_phone_number(phone_number):
    """Normalize a Kenyan phone number into Safaricom's 254 format."""
    cleaned = ''.join(ch for ch in str(phone_number) if ch.isdigit())
    if not cleaned:
        return cleaned

    if cleaned.startswith('254'):
        return cleaned
    if cleaned.startswith('0'):
        return '254' + cleaned[1:]
    if cleaned.startswith('+254'):
        return cleaned.replace('+', '', 1)
    return cleaned


def format_mpesa_amount(amount):
    """Return a valid amount string with two decimal places."""
    return str(Decimal(str(amount)).quantize(Decimal('0.01')))


def generate_mpesa_password(shortcode, passkey, timestamp=None):
    timestamp = timestamp or datetime.utcnow().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{shortcode}{passkey}{timestamp}".encode()
    encoded = base64.b64encode(data_to_encode).decode('utf-8')
    return encoded, timestamp


def get_access_token():
    consumer_key = getattr(settings, 'MPESA_CONSUMER_KEY', '')
    consumer_secret = getattr(settings, 'MPESA_CONSUMER_SECRET', '')
    base_url = getattr(settings, 'MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')

    response = requests.get(
        f"{base_url}/oauth/v1/generate?grant_type=client_credentials",
        auth=(consumer_key, consumer_secret),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get('access_token')


def initiate_stk_push(order, amount, phone_number, account_reference=None, transaction_desc=None):
    access_token = get_access_token()
    shortcode = getattr(settings, 'MPESA_SHORTCODE', '')
    passkey = getattr(settings, 'MPESA_PASSKEY', '')
    callback_url = getattr(settings, 'MPESA_CALLBACK_URL', '')
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    request_body = {
        'BusinessShortCode': shortcode,
        'Password': base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode(),
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(Decimal(str(amount))),
        'PartyA': normalize_phone_number(phone_number),
        'PartyB': shortcode,
        'PhoneNumber': normalize_phone_number(phone_number),
        'CallBackURL': callback_url,
        'AccountReference': account_reference or f'order-{order.id}',
        'TransactionDesc': transaction_desc or f'Order {order.id} payment',
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.post(
        f"{getattr(settings, 'MPESA_BASE_URL', 'https://sandbox.safaricom.co.ke')}/mpesa/stkpush/v1/processrequest",
        json=request_body,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
