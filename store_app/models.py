from django.db import models
# Create your models here.
from django.contrib.auth.models import User
import uuid
from .constants import ORDERSTATUS



class Category(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200)

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 2000','1000 TO 10000'),
        ('10000 TO 20000','10000 TO 20000'),
        ('20000 TO 30000','20000 TO 30000'),
        ('30000 TO 40000','30000 TO 40000'),
        ('40000 TO 50000','40000 TO 50000'),
    )
    price = models.CharField(choices=FILTER_PRICE,max_length=60)
    
# New update
class Product(models.Model):
    STATUS = ('Publish','Publish'),('Draft','Draft')
    
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    colour = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    status=models.CharField(choices=STATUS,max_length=200)
    description = models.TextField(null=True, blank=True)
    information = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.name
    def __str__(self):
        return f"{self.name} (ID: {self.product_id})"
    

class UserProfile(models.Model):
    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    last = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
   
    def __str__(self):
        return self.user.username
    

# Booking/Order Model
# class Booking(models.Model):
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('Confirmed', 'Confirmed'),
#         ('Shipped', 'Shipped'),
#         ('Delivered', 'Delivered'),
#         ('Cancelled', 'Cancelled'),
#     )

#     # Unique booking ID
#     booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

#     # Link to the user placing the booking
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     # Product and cart-related fields
#     cart_items = models.ManyToManyField(Cart)  # Link all cart items to the booking

#     # Booking details
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

#     # Timestamps
#     booked_at = models.DateTimeField(auto_now_add=True)  # Booking date
#     updated_at = models.DateTimeField(auto_now=True)  # Last updated date

#     def __str__(self):
#         return f"Booking {self.booking_id} by {self.user.username} (Status: {self.status})"    

# Order Model
# class Order(models.Model):
#     order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.order_id} by {self.user.username}"
# Start ####
# ORDERSTATUS = ((1,'Design'),(2,'Fusing'),(3,'Making'),(4,'Printing'),(5,'Dispatch'),(6,'Delivery'))
class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_p = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.CharField(max_length=1000,default='')
    status = models.IntegerField(choices=ORDERSTATUS, default=1)
    image = models.FileField(null=True, blank=True)
    quantity = models.IntegerField()
    phone = models.IntegerField() #Extra
    address = models.CharField(max_length=300, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user}"

# # OrderItem Model
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name} (Order: {self.order.order_id})"

#Workers
# class TShirtDesign(models.Model):
#     designer_name = models.CharField(max_length=200)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     design_name = models.CharField(max_length=200)
#     desc = models.TextField()
#     status_choices = [('Submitted', 'Submitted'),('Approved', 'Approved'),('Rejected', 'Rejected'),]
#     status = models.CharField(max_length=20, choices=status_choices, default='Submitted')
#     front_image = models.ImageField(upload_to='designs/front/')
#     back_image = models.ImageField(upload_to='designs/back/')
#     sleeve_image = models.ImageField(upload_to='designs/sleeve/')
#     sample_images = models.FileField(upload_to='designs/samples/')

#     def __str__(self):
#         return self.design_name

#GPT T-Shirt
# class TShirtDesign(models.Model):
#     designer_name = models.CharField(max_length=200)
#     contact = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     profile_pic = models.ImageField(upload_to='designers/profile/', blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     design_name = models.CharField(max_length=200)
#     desc = models.TextField()
#     front_image = models.ImageField(upload_to='designs/front/')
#     back_image = models.ImageField(upload_to='designs/back/', blank=True, null=True)
#     sleeve_image = models.ImageField(upload_to='designs/sleeve/', blank=True, null=True)
#     sample_images = models.FileField(upload_to='designs/samples/', blank=True, null=True) # Add Ahe BHo  field GPT
#     status_choices = [('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
#     status = models.CharField(max_length=20, choices=status_choices, default='Submitted')

#     def __str__(self):
#         return self.design_name

# UPdate Gpt T Shirt Design 
#######    Previ ous  ###########
# class TShirtDesign(models.Model):
#     designer_name = models.CharField(max_length=200)
#     contact = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     profile_pic = models.ImageField(upload_to='designers/profile/', blank=True, null=True, default='designers/icon/87-1024.webp')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     design_name = models.CharField(max_length=200)
#     desc = models.TextField()
#     front_image = models.ImageField(upload_to='designs/front/')
#     back_image = models.ImageField(upload_to='designs/back/', blank=True, null=True)
#     sleeve_image = models.ImageField(upload_to='designs/sleeve/', blank=True, null=True)
#     sample_images = models.ImageField(upload_to='designs/sampler/', blank=True,null=True)    #Multiple img youtube video upload
#     status_choices = [('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
#     status = models.CharField(max_length=20, choices=status_choices, default='Submitted')

#     def __str__(self):
#         return self.design_name
#######    Previ ous  ###########

# class SampleImage(models.Model):
#     image = models.ImageField(upload_to='designs/samples/')
    
# class SampleImage(models.Model):
#     image = models.ImageField(upload_to='designs/samples/')


#     def __str__(self):
#         return f"Sample {self.id}"


# {{{ GPT
ORDERSTATUS = ((1,'Design'),(2,'Fusing'),(3,'Making'),(4,'Printing'),(5,'Dispatch'),(6,'Delivery'))
class Designer(models.Model):
    user = models.ForeignKey (User, on_delete=models.CASCADE, null=True, blank=True)
    designer_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='designer_profiles/', blank=True, null=True)
    role_p = models.IntegerField(choices=ORDERSTATUS, default=1)

    def __str__(self):
        return self.designer_name

class Design(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name="designs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    design_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    desc = models.TextField()
    front_image = models.ImageField(upload_to='design_images/')
    back_image = models.ImageField(upload_to='design_images/', blank=True, null=True)
    sample_images = models.ManyToManyField('SampleImage', blank=True)
    status = models.CharField(max_length=20, choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],default='Submitted')
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.design_name

class SampleImage(models.Model):
    image = models.ImageField(upload_to='sample_images/')

    
# }}}