from django.db import models
from Accounts.models import UserAccount, Address
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random, string

User = get_user_model()

class Wishlist(models.Model):
    
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    sku = models.CharField(max_length=20, db_index=True)  
    product_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    product = GenericForeignKey("product_type", "sku")
    
    def __str__(self):
        return f"{self.user} x {self.product} in Cart"    



class CartStatus(models.TextChoices):  
    PENDING = "PENDING", "PENDING"
    ORDERED = "ORDERED", "ORDERED"
    
class OrderStatus(models.TextChoices):  
    ORDERED = "ORDERED", "ORDERED"
    CANCELED = "CANCELED", "CANCELED"
    SHIPMENT_CREATED = "SHIPMENT_CREATED", "SHIPMENT_CREATED"

class OrderHistoryStatus(models.TextChoices):  
    PENDING = "PENDING", "PENDING"
    PROCESSING = "PROCESSING", "PROCESSING"
    SHIPPED = "SHIPPED", "SHIPPED"
    DELIVERED = "DELIVERED", "DELIVERED"
    CANCELLED = "CANCELLED", "CANCELLED"
    REFUNDED = "REFUNDED", "REFUNDED"


class PaymentMode(models.TextChoices):  
    PG = "PG", "PG"
    COD = "COD", "COD"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    status = models.CharField(
        max_length=10, choices=CartStatus.choices, default=CartStatus.PENDING
    )

    @property
    def value(self):
        return sum(item.item_price() for item in self.cart_items.all())  

    def __str__(self):
        return f"Cart {self.id} ({self.user}) status=({self.status})"

class CartItem(models.Model):
    title=models.CharField(max_length=500)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    sku = models.CharField(max_length=20, db_index=True)  
    product_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    product = GenericForeignKey("product_type", "sku")
    quantity = models.PositiveIntegerField(default=1)

    def item_price(self):
        return self.product.price * self.quantity if self.product else 0  

    def __str__(self):
        return f"{self.quantity} x {self.product} in Cart"

class Order(models.Model):
    order_number = models.CharField(max_length=15, editable=False, unique=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name="order")  # One order per cart
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices)
    
    discount=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    tax=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    packaging_charges=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    handling_charges=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)

    shipping_charges=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    cod_charges=models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    status = models.CharField(max_length=30,choices=OrderStatus.choices,default=OrderStatus.ORDERED)
    
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        return ''.join(random.choices(string.digits, k=15))  

    def __str__(self):
        return f"Order {self.order_number} - {self.user} ({self.payment_mode})"
    
class OrderHistory(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE, related_name='order_history')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="order_histories")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    order_number = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=30)  # COD or Prepaid
    status = models.CharField(max_length=30,choices=OrderHistoryStatus.choices,default=OrderHistoryStatus.PROCESSING)
    

    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    packaging_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    handling_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    cod_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0,null=True,blank=True)
    
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    breadth = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    comment = models.TextField(blank=True, null=True)
    reseller_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    shiprocket_order_id = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderHistory for Order #{self.order_number}"

class OrderHistoryItem(models.Model):
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=500)
    sku = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    product_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product = GenericForeignKey('product_type', 'sku')

    def __str__(self):
        return f"{self.title} (x{self.quantity})"

    def total_price(self):
        return self.selling_price * self.quantity  