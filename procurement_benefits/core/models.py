from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Budget(models.Model):
    classification = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.classification

class CustomUser(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    


# models.py
class SelectedItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)  # Replace 1 with an appropriate default user ID
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"



