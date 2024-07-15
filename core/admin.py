# core/admin.py

from django.contrib import admin
from .models import Item, CustomUser, Department, Budget, SelectedItem, Company

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Item)
admin.site.register(Budget)
admin.site.register(CustomUser)
admin.site.register(SelectedItem)
