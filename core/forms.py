# core/forms.py
from django import forms
from .models import Item, CustomUser, Department, Budget

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'department', 'budget']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['classification', 'amount']
