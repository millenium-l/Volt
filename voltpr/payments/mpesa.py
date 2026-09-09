import base64
from datetime import datetime

import requests

from django.conf import settings


MPESA_AUTH_URL = (
    "https://sandbox.safaricom.co.ke/"
    "oauth/v1/generate"
)

MPESA_STK_PUSH_URL = (
    "https://sandbox.safaricom.co.ke/"
    "mpesa/stkpush/v1/processrequest"
)


def get_access_token():
    response = requests.get(
        MPESA_AUTH_URL,
        params={
            "grant_type": "client_credentials",
        },
        auth=(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET,
        ),
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data["access_token"]


def generate_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def generate_stk_password(timestamp):
    data = (
        f"{settings.MPESA_SHORTCODE}"
        f"{settings.MPESA_PASSKEY}"
        f"{timestamp}"
    )

    password = base64.b64encode(
        data.encode("utf-8")
    ).decode("utf-8")

    return password