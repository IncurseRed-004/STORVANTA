from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Supplier, Category, Product, Purchase, Sale


class UserRegistration(UserCreationForm):
    ROlE_CHOICES =[
        ("manager",'Inventory Manager'),
        ("staff","Sales Staff"),
    ]
    role = forms.ChoiceField(choices=ROlE_CHOICES,widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "role"]

    def save(self, commit=True):
            user =super().save(commit=False)
            role =self.cleaned_data.get("role")
            user.is_manager = role =="manager"
            user.is_sales_staff = role =="staff"
            if commit:
                user.save()
            return user


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =["name","description"]
        widgets ={
            "description": forms.Textarea(attrs={
                "rows":3
            }),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "phone", "email", "address"]
        widgets ={
            "address": forms.Textarea(attrs={
                "rows":3
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "supplier",
            "name",
            "sku",
            "unit_price",
            "stock_quantity",
            "reorder_level",
            "image",
        ]

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["product", "supplier", "quantity", "unit_cost"]

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["product", "customer_name", "quantity", "unit_price"]

    def clean(self):
        cleaned_data =super().clean()
        product = cleaned_data.get("product")
        quantity = cleaned_data.get("quantity")

        if product and quantity:
            if quantity > product.stck_quantity:
                raise forms.ValidationError(
                    f"Not enough stock for {product.name}. Only {product.stck_quantity} left."
                )
        return cleaned_data

