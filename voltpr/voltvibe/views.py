# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .models import Product, Order, OrderItem


# takes a request object and returns a responsethat renders the index.html
# Create your views here.
def index(request):
    return render(request, 'voltvibe/index.html')

def home(request):
    return render(request, 'voltvibe/home.html')
# store
def phone(request):
    #retrieves all product instances from the database
    products = Product.objects.all()
    #Packs the retrieved products into a context dictionary to pass to the template.
    context = {'products':products}
    return render(request, 'voltvibe/phone.html', context)

#for authenticated users
# enables the users to view the cart

#The function cart(request) handles a request, likely from a web application that manages a shopping cart.
def cart(request):
    #checks if the user is authenticated
    if request.user.is_authenticated:
        ''' 1. If the user is authenticated, it retrieves the associated customer object:
			2. request.user: This represents the currently logged-in user. 
            It’s an instance of the user model, which typically includes information like username, email, and authentication status.
        	3. .customer: This part assumes there’s a relationship set up in the database (usually a one-to-one relationship) 
            between the user and a Customer model. So, request.user.customer retrieves the Customer object that is associated with that user.
        '''
        # Retrieve the customer associated with the logged-in user
        customer = request.user.customer
        #It then tries to get an existing order for that customer which is not complete. If no such order exists, it creates a new one:
        '''  it tries to find an existing order for a specific customer that is not complete, and if it doesn't find one, it creates a new order.
		1. Order.objects.get_or_create(...): This is a Django method that attempts to retrieve an object from the database. If it doesn’t exist, it creates a new one.
        2. customer=customer: This specifies that you want to find (or create) an order associated with the given customer.
        3. complete=False: This specifies that you are looking for an order that is marked as incomplete. In other words, you want to find orders that are still in progress and not yet finalized.
        4. order: This variable will hold the order object that was found or the new order object that was created.
        5. created: This is a boolean value (True or False) that indicates whether a new order was created (True) or if an existing order was found (False).
        '''
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #This retrieves all items associated with the order.
        items = order.orderitem_set.all()
        #If the user is not authenticated, an empty list is assigned to items, meaning there are no cart items to display.
    else:
        items = []
	#A context dictionary is created to pass the items to the template so as the users can see what we want to display in the browser:
    context = {'items': items}
    #Finally, it renders the 'cart.html' template, providing it with the context:
    return render(request, 'voltvibe/cart.html', context)


# The function takes two parameters: request, which contains information about the current web request, and product_id, which is the ID of the product to be added to the cart.
def add_to_cart(request, product_id):
    # The code first checks if the user is logged in (is_authenticated). If the user is not logged in, it will redirect them to the login page.
    if request.user.is_authenticated:
        try:
        # Retrieve or create the associated customer object
        # If the user is authenticated, it retrieves the associated customer object.
            customer = request.user.customer
        except Customer.DoesNotExist:
         #Optionally create a new customer or handle this case
            customer = Customer.objects.create(user=request.user)
        # Then, it uses get_or_create to either fetch an existing order for that customer that is not yet complete (complete=False) or create a new one if it doesn't exist.
        # Ensure the user has only one incomplete order (active cart)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # This line retrieves the product using the provided product_id. If the product does not exist, a 404 error is raised.
        product = get_object_or_404(Product, id=product_id)
        
        # Add the product to the cart (order)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            order_item.quantity += 1  # Increment quantity if already exists
            order_item.save()
        
        return redirect('cart')
    else:
        return redirect('login')  # Redirect non-auth users to login

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        order_item = get_object_or_404(OrderItem, id=item_id)
        order_item.delete()
        return redirect('cart')
    else:
        return redirect('login')  # Redirect non-auth users to login

def checkout(request):
	context = {}
	return render(request, 'voltvibe/checkout.html', context)