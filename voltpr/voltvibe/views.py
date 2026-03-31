# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ProductCreateForm
from .models import *
from django.contrib import messages
from .models import Product, Order, OrderItem
from datetime import datetime
from django.utils import timezone
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required


# takes a request object and returns a responsethat renders the index.html
# Create your views here.
def index(request):
    return render(request, 'voltvibe/index.html')

def home(request):
    categories = Product.CATEGORY_CHOICES
    products = Product.objects.all()

    products_page, query = get_filtered_products(request, products)

    return render(request, 'voltvibe/home.html', {
        'categories': categories,
        'products_page': products_page,
        'query': query
    })

#creating a helper function to get the product description by id and render it in the description.html
def get_filtered_products(request, queryset):
    query = request.GET.get('q')
    page = request.GET.get('page', 1)

    # ✅ Apply search filter
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    # ✅ KEEP the filtered queryset, just order it
    queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, 8)
    products_page = paginator.get_page(page)

    return products_page, query


# This function handles the search functionality for products. It retrieves the search query from the request, filters the products based on the query, and returns a JSON response containing the rendered HTML for the filtered product list.
# uses ajax
from django.http import JsonResponse
from django.template.loader import render_to_string

def ajax_products(request):
    category = request.GET.get('category')

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    products_page, query = get_filtered_products(request, products)

    html = render_to_string(
        'voltvibe/partials/product_list.html',
        {'products': products_page},
        request=request
    )

    return JsonResponse({'html': html})


@login_required
def profile(request):
    profile = request.user.profile # access the profile linked to the user
    context = {
        'title': profile,
        'profile': profile,
        'current_year': timezone.now().year,
    }
    return render(request, 'voltvibe/profile.html')

# store

def product_list(request, category):
    products = Product.objects.filter(category=category)

    products_page, query = get_filtered_products(request, products)

    return render(request, 'voltvibe/products.html', {
        'category': category,
        'products_page': products_page,
        'query': query
    })


def description(request, product_id):
     # Fetch the description by ID, or show 404 if not found
    product = get_object_or_404(Product, id=product_id)
    # 'product'is the key used in html and product is the value which is picked from defination function
    context = {'product': product}
    # for users to view
    return render(request, 'voltvibe/description.html', context)


# create product view
@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductCreateForm()

    return render(request, 'voltvibe/create_product.html', {'form': form})


# update product view\
@staff_member_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('description', product_id=product.id)
    else:
        form = ProductCreateForm(instance=product)

    return render(request, 'voltvibe/update_product.html', {'form': form, 'product': product})


@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')



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
    context = {'items': items, 'order': order}
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
        
        if created:
            order_item.quantity = 1
        else:
            order_item.quantity += 1

        order_item.save()
        
        
        
        return redirect('cart')
    

def increase_quantity(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(OrderItem, id=item_id)
        item.quantity += 1
        item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(OrderItem, id=item_id)
        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect('cart')


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
         # Retrieve and delete the order item
        order_item = get_object_or_404(OrderItem, id=product_id)
        order_item.delete()
        return redirect('cart')
    else:
        return redirect('login')  # Redirect non-auth users to login

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        # Calculate the total sum of the order
        total_sum = sum(item.product.price * item.quantity for item in order.orderitem_set.all())

        if request.method == 'POST':
            # Get the name and phone number from the POST request
            name = request.POST.get('name')
            phone_number = request.POST.get('phone_number')

            # Validate the inputs
            if not name or not phone_number:
                messages.error(request, 'Both name and phone number are required.')
            else:
                # Save the data to the order model or a separate model if necessary
                order.customer_name = name
                order.customer_phone = phone_number
                order.save()

                # Proceed to payment (for now, just a success message)
                return redirect('payment')  # Redirect to payment page (or your payment logic here)

        context = {
            'order': order,
            'total_sum': total_sum,
        }
        return render(request, 'voltvibe/checkout.html', context)
    else:
        return redirect('login')  # Redirect non-auth users to login