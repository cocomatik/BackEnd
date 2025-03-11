from django.db import models
from cloudinary.models import CloudinaryField  # For Cloudinary Image Uploads

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class POCOS(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=False, blank=False)  # Better for large text
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Precise for currency values
    stock = models.PositiveIntegerField(default=0)  # Ensures non-negative stock values
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=255, null=True, blank=True)  # Optional brand
    image = CloudinaryField('image', folder='pocos/')  # Cloudinary image storage
    rating = models.FloatField(default=0.0)  # Average rating value
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest products first

    def __str__(self):
        return self.title
