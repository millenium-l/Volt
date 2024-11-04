from django.db import models
from django.contrib.auth.models import User

# Create your models here.

''' Customer Model: Represents each authenticated user who wants to shop at your store. 
    Each Customer instance is linked to a user account through a one-to-one relationship 
    with Django's built-in User model.  
'''
class Customer(models.Model):
    #a one-to-one relationship with Django's built-in User model, allowing each customer to have a corresponding user account. If the user is deleted, the associated customer will also be deleted due to
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    #unique=True constraint to the email field to prevent duplicate email entries.
    email = models.CharField(max_length=200, unique=True)

    #str method: Returns the customer's name for easy identification.
    def __str__(self):
        return self.name

''' Product Model: Used to store information about each product available in your store. 
    This model holds details like the product's name, price, whether it's a digital product, and its image. 
'''
class Product(models.Model):
    name = models.CharField(max_length=200)
    # ensuring non-negative values we use (default=0.0)
    price = models.FloatField(default=0.0)
    digital = models.BooleanField(default=False,null=True, blank=True)
    #we have to pip install pillow to handle images
    image = models.ImageField(null=True, blank=True)
    #str method: Returns the product's name for easy identification.
    def __str__(self):
        return self.name

''' Order Model: Represents every order made by the user. 
    Each Order instance is linked to a Customer, allowing you to track which customer placed the order, 
    along with details such as the order date and completion status. 
'''
# it is a finished order
class Order(models.Model):
    #a foreign key linking to the Customer model. If the customer is deleted, the order will not be deleted; instead, the customer field will be set to null.
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    #a datetime field that automatically records when the order is created.
    date_ordered = models.DateTimeField(auto_now_add=True)
    #a boolean field indicating whether the order is completed.
    complete = models.BooleanField(default=False)
    #a character field for storing the transaction ID, allowing null values.
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

''' OrderItem Model: Stores each individual product that is part of an order. 
    It links to both the Product and Order models, allowing you to specify the quantity of each product ordered 
    and when it was added to the order. 
'''
# its like the cart since it is an unfinished order
class OrderItem(models.Model):
    # A foreign key linking to the Product model. If the product is deleted, the order item will not be deleted; instead, it will be set to null.
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
     