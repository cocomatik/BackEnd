from django.db import models
from cloudinary.models import CloudinaryField
import random
from django.core.validators import MinValueValidator, MaxValueValidator
import string

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True,primary_key=True)  

    def __str__(self):
        return self.name

class POJOS(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pojos',to_field='name', db_index=True)
    brand = models.CharField(max_length=255, null=True, blank=True)

    pojo_id = models.CharField(max_length=20, unique=True, blank=True, editable=False, db_index=True,primary_key=True)

    display_image = CloudinaryField('image', folder='pojos/display/')

    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    size = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def discount(self):
        """Calculate discount percentage ((MRP - Price) / MRP) * 100"""
        if self.mrp > 0 and self.mrp > self.price:
            return round(((self.mrp - self.price) / self.mrp) * 100, 2)
        return 0.0
    def generate_pojo_id(self,length=15):
        """Generate a random alphanumeric + URL-safe special character ID of given length."""
        characters = string.ascii_letters + string.digits + "-_~!@%^*"
        return ''.join(random.choices(characters, k=length))

    def save(self, *args, **kwargs):
        if not self.pojo_id:
            self.pojo_id = self.generate_pojo_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.pojo_id})"

class PojoImage(models.Model):
    pojo = models.ForeignKey(POJOS, on_delete=models.CASCADE, related_name='extra_images')
    image = CloudinaryField('image', folder='pojos/extra/')

    def __str__(self):
        return f"{self.pojo.title} - Extra Image {self.id}"

class Review(models.Model):
    pojo = models.ForeignKey(POJOS, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=255)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    verified_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} - {self.pojo.title} ({self.rating})"
