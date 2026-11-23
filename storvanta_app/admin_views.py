from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from storvanta_app.decorators import admin_required
from storvanta_app.forms import UserRegistration
from storvanta_app.models import Login


@admin_required
def user_list(request):
    users = Login.objects.all().order_by("username")
    return render(request, "admin/user_list.html", {"users": users})

@admin_required
def user_create(request):
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f"User '{new_user.username}' created as {new_user.role_name}.")
            return redirect("user_list")
    else:
        form = UserRegistration()
    return render(request, "form.html", {"form": form, "title": "Create User"})

@admin_required
@require_POST
def user_delete(request, pk):
    target_user =get_object_or_404(Login,pk=pk)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own user")
        return redirect("user_list")
    target_user.delete()
    messages.success(request, "User deleted successfully")
    return redirect("user_list")
