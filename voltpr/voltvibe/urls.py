from django.urls import path
from .views import index, home, phone, description, cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('index/', index, name='index'),
    path('home/', home, name='home'),
    path('phone/', phone, name='phone'),
    path('description/<int:product_id>/', description, name='description'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]