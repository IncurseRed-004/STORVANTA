from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from storvanta_app.decorators import sales_or_admin_required
from storvanta_app.forms import SalesForm
from storvanta_app.models import Sale, Product


@sales_or_admin_required
def sales_list(request):
    sales = Sale.objects.select_related('product','sold_by').all()
    return render(request,"sales_list.html",{"sales":sales})

@sales_or_admin_required
def  sales_create(request):
    if request.method =="POST":
        form =SalesForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                product =Product.objects.select_for_update().get(pk=sale.product.pk)


                if sale.quantity > product.stock_quantity:
                    messages.error(request,f"Only {product.stock_quantity} units of {product.name} are available.")
                    return render(request,"sale_form.html",{"form":form,"title":"form for sale"})

                sale.sold_by = request.user
                sale.save()
                product.stock_quantity -= sale.quantity
                product.save()
                messages.success(request,f"Sale recorded: {sale.quantity} x {product.name} (Total: ₹{sale.total_amount}).")
                return redirect('sales_list')
    else:
        form =SalesForm()
    return render(request,"sales_form.html",{"form":form,"title":"record sale"})