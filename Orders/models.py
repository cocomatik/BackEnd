from django.db import models
from Accounts.models import UserAccount, Address
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import random, string

User = get_user_model()

class CartStatus(models.TextChoices):  
    ORDERED = "ORDERED", "ORDERED"
    PENDING = "PENDING", "PENDING"
    
class OrderStatus(models.TextChoices):  
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
    sku = models.CharField(max_length=20, db_index=True)  # SKU instead of object_id
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
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30,choices=OrderStatus.choices,default=OrderStatus.PENDING)
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



class OrderedCart(models.Model):
    STATUS_CHOICES = (
        ("FAIL", "Fail"),
        ("SUCCESS", "Success"),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="ordered_cart")
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    shiprocket_order_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="FAIL")
    remark = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OrderedCart #{self.id} - {self.order.user} - {self.status}"
    

class OrderedCartItem(models.Model):
    ordered_cart = models.ForeignKey(OrderedCart, on_delete=models.CASCADE, related_name="ordered_items")
    sku = models.CharField(max_length=20, db_index=True)
    product_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    product = GenericForeignKey("product_type", "sku")
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
