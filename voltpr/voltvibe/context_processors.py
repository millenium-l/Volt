from .models import Order


def cart_count(request):
    """Expose a cart item count for authenticated users in all templates."""
    count = 0

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Exception:
            customer = None

        if customer:
            order = Order.objects.filter(customer=customer, complete=False).first()
            if order:
                count = order.get_cart_items or 0

    return {
        'cart_count': count
    }
from .models import Order


def cart_count(request):
    """Expose a cart item count for authenticated users in all templates."""
    count = 0

    if request.user.is_authenticated:
        try:
            customer = request.user.customer
        except Exception:
            customer = None

        if customer:
            order = Order.objects.filter(customer=customer, complete=False).first()
            if order:
                count = order.get_cart_items or 0

    return {
        'cart_count': count
    }
