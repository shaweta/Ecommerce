from django.contrib import admin
from .models import Product,Variation,ReviewRatings

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields= {"slug":("product_name",)}
    list_display=("product_name","price","stock","category","is_available","modified_date")

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRatings)
