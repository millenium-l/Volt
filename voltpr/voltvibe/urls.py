from django.urls import path
from .views import index, home, phone,profile, description, cart, add_to_cart, remove_from_cart, checkout, increase_quantity, decrease_quantity

urlpatterns = [
    path('index/', index, name='index'),
    path('home/', home, name='home'),
    path('phone/', phone, name='phone'),
    path('profile/', profile, name='profile'),
    path('description/<int:product_id>/', description, name='description'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('increase-quantity/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
]