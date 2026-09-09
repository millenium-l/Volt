import requests

from django.conf import settings


MPESA_AUTH_URL = (
    "https://sandbox.safaricom.co.ke/"
    "oauth/v1/generate"
)

# Get M-Pesa access token
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