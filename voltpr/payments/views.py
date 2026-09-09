import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .mpesa import initiate_stk_push


@require_POST
def stk_push(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON body."},
            status=400,
        )

    phone_number = data.get("phone_number")
    amount = data.get("amount")
    account_reference = data.get("account_reference")
    transaction_description = data.get("transaction_description")

    if not phone_number:
        return JsonResponse(
            {"error": "phone_number is required."},
            status=400,
        )

    if not amount:
        return JsonResponse(
            {"error": "amount is required."},
            status=400,
        )

    if not account_reference:
        return JsonResponse(
            {"error": "account_reference is required."},
            status=400,
        )

    if not transaction_description:
        return JsonResponse(
            {"error": "transaction_description is required."},
            status=400,
        )

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "amount must be a whole number."},
            status=400,
        )

    if amount <= 0:
        return JsonResponse(
            {"error": "amount must be greater than zero."},
            status=400,
        )

    try:
        response = initiate_stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=account_reference,
            transaction_description=transaction_description,
        )

        return JsonResponse(response, status=200)

    except Exception as error:
        return JsonResponse(
            {
                "error": "Failed to initiate STK Push.",
                "details": str(error),
            },
            status=500,
        )