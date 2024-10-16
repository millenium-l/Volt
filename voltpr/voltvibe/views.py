# Create your views here.
from django.shortcuts import render
'''to store details to the database '''


# Create your views here.
def index(request):
    return render(request, 'voltvibe/index.html')

def home(request):
    return render(request, 'voltvibe/home.html')

def phone(request):
    return render(request, 'voltvibe/phone.html')
