"""
URL configuration for procurement_benefits project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', views.settings, name='settings'),
    path('view_all_items/', views.view_all_items, name='view_all_items'),
    path('', views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('user_home/', views.user_home, name='user_home'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/update/<int:item_id>/', views.update_item, name='update_item'),
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/update/<int:user_id>/', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('edit_departments/', views.edit_departments, name='edit_departments'),
    path('departments/update/<int:department_id>/', views.update_department, name='update_department'),
    path('departments/delete/<int:department_id>/', views.delete_department, name='delete_department'),
    path('select_item/', views.select_item, name='select_item'),
    path('settings/', views.settings, name='settings'),
    path('summary_checkout/', views.summary_checkout, name='summary_checkout'),
    path('add_budget/', views.add_budget, name='add_budget'),
    path('view_budgets/', views.view_budgets, name='view_budgets'),
    path('update_budget/<int:budget_id>/', views.update_budget, name='update_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
]