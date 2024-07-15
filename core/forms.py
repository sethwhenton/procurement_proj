# core/forms.py

from django import forms
from .models import Item, CustomUser, Department, Budget, Company

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'department', 'company']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'company']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['classification', 'amount', 'company']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']
