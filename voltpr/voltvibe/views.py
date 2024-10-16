# Create your views here.
from django.shortcuts import render
from .models import *


# Create your views here.
def index(request):
    return render(request, 'voltvibe/index.html')

def home(request):
    return render(request, 'voltvibe/home.html')
# store
def phone(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'voltvibe/phone.html', context)
