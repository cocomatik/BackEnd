from django.db import models
from decimal import Decimal

class Revenue(models.Model):
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=100, decimal_places=2, default= Decimal(0.00))

    def __str__(self):
        return f"{self.date}  ₹{self.total_revenue}"



# from django.db import models
# from decimal import Decimal

# class Revenue(models.Model):
#     month = models.PositiveSmallIntegerField()  # 1 = Jan, 12 = Dec
#     year = models.PositiveIntegerField()
#     date = models.DateField()  # Typically first of the month or any date in the month
#     total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
#     total_orders = models.PositiveIntegerField(default=0)
#     average_order_value = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
#     growth_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # in percentage

#     class Meta:
#         unique_together = ('month', 'year')
#         ordering = ['year', 'month']

#     def __str__(self):
#         return f"{self.month:02d}/{self.year} - ₹{self.total_revenue}"
