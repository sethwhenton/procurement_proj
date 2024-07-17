from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='items', null=True)

class Budget(models.Model):
    classification = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.classification

class CustomUser(models.Model):  # Changed from AbstractUser to models.Model
    name = models.CharField(max_length=100)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    budget = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        return self.namee

class SelectedItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"
