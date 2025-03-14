from django.db import models
from cloudinary.models import CloudinaryField
import random
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)  # Indexed for faster lookups

    def __str__(self):
        return self.name

class POCOS(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pocos', db_index=True)
    brand = models.CharField(max_length=255, null=True, blank=True)

    poco_id = models.CharField(max_length=6, unique=True, blank=True, editable=False, db_index=True,primary_key=True)

    display_image = CloudinaryField('image', folder='pocos/display/')

    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    size = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_poco_id(self):
        """Generate a 6-digit unique Poco ID."""
        while True:
            random_id = str(random.randint(100000, 999999))
            if not POCOS.objects.filter(poco_id=random_id).exists():
                return random_id

    def save(self, *args, **kwargs):
        if not self.poco_id:
            self.poco_id = self.generate_poco_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.poco_id})"

class PocoImage(models.Model):
    poco = models.ForeignKey(POCOS, on_delete=models.CASCADE, related_name='extra_images')
    image = CloudinaryField('image', folder='pocos/extra/')

    def __str__(self):
        return f"{self.poco.title} - Extra Image {self.id}"

class Review(models.Model):
    poco = models.ForeignKey(POCOS, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=255)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    verified_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name} - {self.poco.title} ({self.rating})"
