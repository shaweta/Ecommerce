from django.contrib import admin
from .models import Product,Variation,ReviewRatings,ProductGallery
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):
    model=ProductGallery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {"slug":("product_name",)}
    list_display=("product_name","price","stock","category","is_available","modified_date")
    inlines=[ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRatings)
admin.site.register(ProductGallery)
