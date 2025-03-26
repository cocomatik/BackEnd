from django.contrib import admin
from .models import POJOS, Category, PojoImage, Review

class PojoImageInline(admin.TabularInline):
    model = PojoImage
    extra = 2  

@admin.register(POJOS)
class POJOSAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'price', 'stock', 'category', 'created_at')
    search_fields = ('title', 'sku')  
    list_filter = ('category', 'created_at')  
    readonly_fields = ('sku',)  
    inlines = [PojoImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pojo_count')

    def pojo_count(self, obj):
        return obj.pojos.count()  
    pojo_count.short_description = "Number of POJOS"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'pojo', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_name', 'pojo__title')  

from .modelsxs import (
    FeatureProducts, BestSellers, BestOfWeddingJewellery, BestOfPendants,
    BestOfNoseRings, BestOfNecklace, BestOfOneGramGoldenJewellery, BestOfImportedJewellery,
    BestOfFingerRings, BestOfEarRings, BestOfChains, BestOfBracelets, BestOfBangles
)

admin.site.register(FeatureProducts)
admin.site.register(BestSellers)
admin.site.register(BestOfWeddingJewellery)
admin.site.register(BestOfPendants)
admin.site.register(BestOfNoseRings)
admin.site.register(BestOfNecklace)
admin.site.register(BestOfOneGramGoldenJewellery)
admin.site.register(BestOfImportedJewellery)
admin.site.register(BestOfFingerRings)
admin.site.register(BestOfEarRings)
admin.site.register(BestOfChains)
admin.site.register(BestOfBracelets)
admin.site.register(BestOfBangles)
