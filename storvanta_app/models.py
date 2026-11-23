import decimal
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT


class Login(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_sales_staff = models.BooleanField(default=False)

    @property
    def role_name(self):
        if self.is_staff or self.is_manager:
            return 'Admin'
        if self.is_manager:
            return 'Inventory Manager'
        if self.is_sales_staff:
            return 'Sales Staff'
        return "User"

    def __str__(self):
        return f"{self.username} ({self.role_name}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank =True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at =models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT,related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null =True,blank=True,related_name='products')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100,unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators =[MinValueValidator(Decimal("0.01"))])
    stock_quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    image = models.FileField(upload_to="products/", blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level

    def __str__(self):
        return f"{self.name} ({self.sku}"

class Purchase(models.Model):
    product =models.ForeignKey(Product, on_delete=PROTECT, related_name='purchases')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,null =True, related_name='purchases')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    total_cost = models.DecimalField(max_digits=12,decimal_places=2,editable=False)
    purchased_by = models.ForeignKey(Login, on_delete=models.SET_NULL,null=True, related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self,*args,**kwargs):
        self.total_cost = Decimal(self.quantity) *  self.unit_cost
        super().save(*args,**kwargs)

    def __str__(self):
        return f"Purchase #{self.id} - {self.product.name} (+{self.quantity})"


class Sale(models.Model):
    product =models.ForeignKey(Product,on_delete=models.CASCADE,related_name='sales')
    customer_name = models.CharField(max_length=150,blank=True,null=True,default="walk_-in Customer")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal(0.01))])
    total_amount = models.DecimalField(max_digits=12,decimal_places=2,editable=False)
    sold_by = models.ForeignKey(Login, on_delete=models.SET_NULL,null=True, related_name='sales')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =["-created_at"]

    def save(self, *args, **kwrgs):
        self.total_amount =Decimal(self.quantity) * self.unit_price
        super().save(*args,**kwrgs)

    def __str__(self):
        return f"Sale #{self.id} - {self.product.name} (-{self.quantity})"