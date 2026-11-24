from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth

from storvanta_app.models import Product, Purchase, Sale, Category


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username =request.POST.get("username")
        password =request.POST.get("password")
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request,"Invalid username and/or password.")

    return render(request, "login.html")


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out")
    return redirect("login")

@login_required(login_url="login")
def dashboard(request):
    # 1. KPI Summary Metrics
    total_products = Product.objects.count()
    low_stock_products = (
        Product.objects.select_related("category")
        .filter(stock_quantity__lte=F("reorder_level"))
        .order_by("stock_quantity")
    )
    low_stock_count = low_stock_products.count()
    total_sales = Sale.objects.aggregate(total=Sum("total_amount"))["total"] or 0
    total_purchases = Purchase.objects.aggregate(total=Sum("total_cost"))["total"] or 0

    # 2. Monthly Sales vs. Purchases (for Chart.js bar/line chart)
    monthly_sales_qs = (
        Sale.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )
    monthly_purchases_qs = (
        Purchase.objects.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_cost"))
        .order_by("month")
    )

    sales_by_month = {row["month"]: float(row["total"]) for row in monthly_sales_qs if row["month"]}
    purchases_by_month = {row["month"]: float(row["total"]) for row in monthly_purchases_qs if row["month"]}
    all_months = sorted(set(sales_by_month.keys()) | set(purchases_by_month.keys()))

    month_labels = [m.strftime("%b %Y") for m in all_months]
    sales_series = [sales_by_month.get(m, 0) for m in all_months]
    purchases_series = [purchases_by_month.get(m, 0) for m in all_months]

    # 3. Product Distribution by Category (for Chart.js doughnut chart)
    category_qs = Category.objects.annotate(product_count=Count("products")).order_by("name")
    category_labels = [c.name for c in category_qs]
    category_counts = [c.product_count for c in category_qs]

    context = {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "low_stock_products": low_stock_products,
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "month_labels": month_labels,
        "sales_series": sales_series,
        "purchases_series": purchases_series,
        "category_labels": category_labels,
        "category_counts": category_counts,
    }
    return render(request, "dashboard.html", context)

