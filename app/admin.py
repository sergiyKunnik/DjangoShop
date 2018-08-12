from django.contrib import admin
from .models import Category, Product, CartItem, Cart, Order, ProductImages
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ProductImages)
