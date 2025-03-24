from django.db import models
from Accounts.models import UserAccount, Address
from POCOS.models import POCOS
from POJOS.models import POJOS
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random,string
User = get_user_model()

class CartStatus(models.TextChoices):  
    ORDERED = "ordered", "Ordered"
    PENDING = "pending", "Pending"

class PaymentMode(models.TextChoices):  
    PG = "paymentgateway", "Payment Gateway"
    COD = "cashondelivery", "Cash On Delivery"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    status = models.CharField(
        max_length=10, choices=CartStatus.choices, default=CartStatus.PENDING
    )
    
    @property
    def value(self):
        return sum(item.item_price() for item in self.cart_items.all())  # Fixed related_name

    def __str__(self):
        return f"Cart {self.id} ({self.user})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # POCOS or POJOS
    object_id = models.CharField(max_length=15)
    product = GenericForeignKey("content_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)

    def item_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product} in Cart"

class Order(models.Model):
    order_number = models.CharField(max_length=15, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="orders")
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
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