from django.contrib import admin
from .models import POCOS, Category, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2  # Number of blank extra image fields

@admin.register(POCOS)
class POCOSAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'created_at')
    inlines = [ProductImageInline]

admin.site.register(Category)
