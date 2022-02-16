from django.contrib import admin
from .models import Product, Variation, ReviewRating

# Register your models here.

### we have to make way for slug auto populate
class ProductAdmin(admin.ModelAdmin):
  ### this is what will display at the admin side about each product for us to see
  list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
  ## pre populated field
  prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
  list_display   = ('product', 'variation_category', 'variation_value', 'is_active')
  list_editable  = ('is_active',)
  list_filter    = ('product', 'variation_category', 'variation_value')



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)




#### we see the store app and we see products under it that we can add products but store is the bigger app