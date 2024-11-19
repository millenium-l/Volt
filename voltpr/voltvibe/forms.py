# manage form behavious
# Django's inbuilt form

from django import forms
from .models import OrderItem

# in the meta class is where we can define our own ProductCreateform
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
