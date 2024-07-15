# core/urls.py

from django.contrib import admin
from django.urls import path
from core import views


urlpatterns = [
    path('', views.main_home, name='main_home'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),  # Ensure this line is present
    path('admin_home/', views.admin_home, name='admin_home'),
    path('settings/', views.settings, name='settings'),

    
    path('view_all_items/', views.view_all_items, name='view_all_items'),
    path('select_department/', views.select_department, name='select_department'),
    path('items_per_department/<int:department_id>/', views.items_per_department, name='items_per_department'),
    path('view_total_items/', views.view_total_items, name='view_total_items'),
    path('download_excel/', views.download_excel, name='download_excel'),

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

    path('add_budget/', views.add_budget, name='add_budget'),
    path('view_budgets/', views.view_budgets, name='view_budgets'),
    path('update_budget/<int:budget_id>/', views.update_budget, name='update_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),

    path('main_home/', views.main_home, name='main_home'),
    path('add_new_company/', views.add_new_company, name='add_new_company'),
    path('update_company_name/<int:company_id>/', views.update_company_name, name='update_company_name'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),

    path('user_home/', views.user_home, name='user_home'),
    path('select_item/', views.select_item, name='select_item'),
    path('save_selection/', views.save_selection, name='save_selection'),
    path('summary_checkout/', views.summary_checkout, name='summary_checkout'),
    path('user_selected_items/', views.user_selected_items, name='user_selected_items'),
]