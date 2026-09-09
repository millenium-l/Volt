from django.urls import path

from .views import initiate_payment, mpesa_callback, payment_page


app_name = 'payments'

urlpatterns = [
    path('<int:order_id>/', payment_page, name='payment_page'),
    path('initiate/<int:order_id>/', initiate_payment, name='initiate'),
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
]