from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def admin_required(view_func):
    @login_required(login_url="login")
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, "You do not have permission to access that admin page.")
        return redirect("dashboard")
    return wrapper

def manager_or_admin_required(view_func):
    @login_required(login_url="login")
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser or request.user.is_manager:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Only Inventory Managers or Admins can access that page.")
        return redirect("dashboard")
    return wrapper

def sales_or_admin_required(view_func):
    @login_required(login_url="login")
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser or request.user.is_sales_staff:
            return view_func(request, *args, **kwargs)
        messages.error(request, "Only Sales Staff or Admins can access that page.")
        return redirect("dashboard")
    return wrapper