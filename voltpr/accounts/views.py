#  Ensure you have all necessary imports, including forms and User.
from django import forms  # Don't forget this import
from django.contrib.auth.models import User  # Import User model
# we import necessary functions and forms from django
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add the email field

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include the new field


# Create your views here.
# handles user registration

# The register view now uses CustomUserCreationForm instead of the standard UserCreationForm, allowing for the email field to be included in the registration process.
def register(request):
    # this means the user is trying to submit the registration form
    if request.method == 'POST':
        # if the form is valid, user logs in and redirects to signin
        # we use request.post since we just want to save the data
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    # If it's not a POST request (meaning the user just opened the page), it creates a new, empty registration form.    
    else:
        form = CustomUserCreationForm()

    #  Finally, it renders the account.html template, passing the form to the template so the user can fill it out.
    return render(request, 'accounts/register.html', {'form': form})
        
def user_login(request):
    if request.method == 'POST':
        # since we want to use the data in user creation we save the data in a data variable
        form = AuthenticationForm(request, data=request.POST)
        # if form is valid we use the get user from the register
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form':form})

def user_logout(request):
      logout(request)
      return redirect('login')  
