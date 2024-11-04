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
'''  Function Definition ==> This defines a function named register that takes a request object as an argument. This object contains information about the HTTP request made to the server.
 '''
# takes a request as an argument and returns a http response
def register(request):
    # This checks if the request method is POST, which indicates that the user is submitting the registration form.
    if request.method == 'POST':
        # if the form is valid, user logs in and redirects to signin
        # we use request.post since we just want to save the data
        form = CustomUserCreationForm(request.POST)
        # The code checks if the form is valid.
        if form.is_valid():
            # If the form is valid, it saves the new user to the database.
            user = form.save()
            # After saving the user, the code logs them in automatically, establishing a session for that user.
            login(request, user)
            # After successful registration and login, the user is redirected to the login page 
            return redirect('login')
        
        ''' Handling GET request ==> If the request method is not POST, it creates an empty instance of the registration form. This typically happens when the user first visits the registration page. '''
    # If it's not a POST request (meaning the user just opened the page), it creates a new, empty registration form.    
    else:
        form = CustomUserCreationForm()

    #  Finally, it renders the account.html template, passing the form to the template so the user can fill it out.
    # allows the user to see the form.
    return render(request, 'accounts/register.html', {'form': form})

# This defines the user_login function, which takes request as an argument. The request object contains information about the user's request, including any submitted data.   
def user_login(request):
    # Here, we check if the request method is POST. This indicates that the user has submitted the login form.
    if request.method == 'POST':
        ''' 1.since we want to use the data in user creation we save the data in a data variable
            2. An AuthenticationForm is instantiated with the request and the submitted data (request.POST). This form is responsible for validating the user’s credentials.
        '''
        form = AuthenticationForm(request, data=request.POST)
        # if form is valid we use the get user from the register
        if form.is_valid():
            # get_user() retrieves the user associated with the provided credentials. 
            user = form.get_user()
            # The login() function then logs the user into the session, allowing them to access authenticated views.
            login(request, user)
            return redirect('home')
        
        # Handles GET request
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form':form})

def user_logout(request):
      logout(request)
      return redirect('home')  



# The GET and POST are two HTTP methods used for sending and receiving data between the client (like a web browser) and the server.
# GET ==> Typically used to retrieve data from the server.
# POST ==> Used to submit data to the server, often for creating or updating resources.