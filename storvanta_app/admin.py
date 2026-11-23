from django.contrib import admin
from .models import Category, Login, Product, Purchase, Sale, Supplier

admin.site.register(Category)
admin.site.register(Login)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Supplier)