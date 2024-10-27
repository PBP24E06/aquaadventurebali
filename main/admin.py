from django.contrib import admin
from main.models import Product
from main.models import Forum

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'harga')  # Remove 'created_at' if it doesn't exist
    list_link = ('id', 'name')
    list_filter = ('harga',)  # Add comma to make it a tuple
    search_fields = ('name', 'harga')  # Use 'harga' instead of 'price'
    ordering = ('harga',)  # Use 'harga' for ordering

admin.site.register(Product, ProductAdmin)
admin.site.register(Forum)
