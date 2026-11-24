from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from storvanta_app.decorators import manager_or_admin_required
from storvanta_app.forms import CategoryForm, SupplierForm, ProductForm, PurchaseForm
from storvanta_app.models import Category, Supplier, Product, Purchase


@manager_or_admin_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'manager/category_list.html', {'categories': categories})


@manager_or_admin_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Added Successfully")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Category'})


@manager_or_admin_required
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'manager/supplier_list.html', {'suppliers': suppliers})


@manager_or_admin_required
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier Added Successfully")
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Supplier'})


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.select_related('category', 'supplier').all()
    return render(request, 'manager/product_list.html', {'products': products})


@manager_or_admin_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Added Successfully")
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'form.html', {'form': form, 'title': 'Add Product'})


@manager_or_admin_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product edited successfully")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'form.html', {'form': form, 'title': f'Edit {product.name}'})


@manager_or_admin_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('product_list')


@manager_or_admin_required
def purchase_list(request):
    purchases = Purchase.objects.select_related('product', 'supplier', 'purchased_by').all()
    return render(request, 'manager/purchase_list.html', {'purchases': purchases})


@manager_or_admin_required
def purchase_create(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)
                purchase.purchased_by = request.user
                purchase.save()

                product = Product.objects.select_for_update().get(pk=purchase.product.pk)
                product.stock_quantity += purchase.quantity
                product.save()

            messages.success(request, f"Recorded purchase of {purchase.quantity} x {product.name}. Stock updated.")
            return redirect('purchase_list')
    else:
        form = PurchaseForm()
    return render(request, 'form.html', {'form': form, 'title': 'Record Purchase'})