from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('checkout_request_id', 'receipt_number', 'phone_number')