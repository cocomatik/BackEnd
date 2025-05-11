from django.db import models
from decimal import Decimal

class Revenue(models.Model):
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=100, decimal_places=2, default= Decimal(0.00))

    def __str__(self):
        return f"{self.date}  ₹{self.total_revenue}"



