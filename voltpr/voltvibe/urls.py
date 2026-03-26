from django.urls import path
from .views import index, home, profile, description, cart, add_to_cart, remove_from_cart, checkout, increase_quantity, decrease_quantity, product_list, ajax_products, create_product, update_product

urlpatterns = [
    path('index/', index, name='index'),
    path('home/', home, name='home'),
    path('ajax_products/', ajax_products, name='ajax_products'),
    path('products/<str:category>/', product_list, name='product_list'),
    path('profile/', profile, name='profile'),
    path('description/<int:product_id>/', description, name='description'),

    # Admin crud URLs
    path('create_product/', create_product, name='create_product'),
    path('update_product/<int:product_id>/', update_product, name='update_product'),



    # Cart and Checkout URLs
    path('cart/', cart, name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('increase-quantity/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:item_id>/', decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
]