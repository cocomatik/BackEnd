from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class POCOS(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.CharField(max_length=255, null=True, blank=True)
    
    # Display Image (Primary Image)
    display_image = CloudinaryField('image', folder='pocos/display/')

    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(POCOS, on_delete=models.CASCADE, related_name='extra_images')
    image = CloudinaryField('image', folder='pocos/extra/')

    def __str__(self):
        return f"{self.product.title} - Extra Image {self.id}"
