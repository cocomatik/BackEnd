from django.contrib import admin
from .models import POCOS, Category, PocoImage, Review

class PocoImageInline(admin.TabularInline):
    model = PocoImage
    extra = 2  

@admin.register(POCOS)
class POCOSAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'price', 'stock', 'category', 'created_at')
    search_fields = ('title', 'sku')  
    list_filter = ('category', 'created_at')  
    readonly_fields = ('sku',)  
    inlines = [PocoImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'poco_count')

    def poco_count(self, obj):
        return obj.pocos.count()  
    poco_count.short_description = "Number of POCOS"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'poco', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'poco__title')  

from .modelsxs import (
    FeatureProducts, BestSellers, BestOfSkinCare,
    BestOfImportedProducts, BestOfHairCare, BestOfFragrance,
    BestOfColorCosmetic, BestOfBodyCare
)

# Registering all category models separately
admin.site.register(FeatureProducts)
admin.site.register(BestSellers)
admin.site.register(BestOfSkinCare)
admin.site.register(BestOfImportedProducts)
admin.site.register(BestOfHairCare)
admin.site.register(BestOfFragrance)
admin.site.register(BestOfColorCosmetic)
admin.site.register(BestOfBodyCare)
