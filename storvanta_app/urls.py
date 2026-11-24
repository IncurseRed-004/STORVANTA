from django.urls import path
from . import views, admin_views, manager_views, staff_views

urlpatterns = [
    # views.py
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # admin_views.py
    # User Management
    path('users/', admin_views.user_list, name='user_list'),
    path('users/create/', admin_views.user_create, name='user_create'),
    path('users/<int:pk>/delete/', admin_views.user_delete, name='user_delete'),

    #manager_views.py
    # CATEGORY
    path('categories/', manager_views.category_list, name='category_list'),
    path('categories/add/', manager_views.add_category, name='category_create'),

    # SUPPLIER
    path('suppliers/', manager_views.supplier_list, name='supplier_list'),
    path('suppliers/add/', manager_views.supplier_create, name='supplier_create'),

    # PRODUCT
    path('products/', manager_views.product_list, name='product_list'),
    path('products/add/', manager_views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', manager_views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', manager_views.product_delete, name='product_delete'),

    # PURCHASE
    path('purchases/', manager_views.purchase_list, name='purchase_list'),
    path('purchases/add/', manager_views.purchase_create, name='purchase_create'),

#     staff_views.py
    # SALES
    path('sales/', staff_views.sales_list, name='sale_list'),
    path('sales/add/', staff_views.sales_create, name='sale_create'),

]