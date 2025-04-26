from django.db import models
from Orders.models import Order

# Create your models here.
class ShiprocketOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shiprocket_order_id = models.BigIntegerField()
    shipment_id = models.BigIntegerField()
    status = models.CharField(max_length=50)
    status_code = models.CharField(max_length=50)
    awb_code = models.CharField(max_length=50)
    courier_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f"{self.id} - order {self.order}  - shiprocket order - {self.shiprocket_order_id}")
