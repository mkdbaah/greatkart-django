from django.contrib import admin
from .models import Product

# Register your models here.

### we have to make way for slug auto populate
class ProductAdmin(admin.ModelAdmin):
  ### this is what will display at the admin side about each product for us to see
  list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
  ## pre populated field
  prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)




#### we see the store app and we see products under it that we can add products but store is the bigger app