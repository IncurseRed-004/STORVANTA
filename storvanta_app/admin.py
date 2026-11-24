from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Login, Product, Purchase, Sale, Supplier


@admin.register(Login)
class LoginAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_manager", "is_sales_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("STORVANTA Roles", {"fields": ("is_manager", "is_sales_staff")}),
    )


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Supplier)