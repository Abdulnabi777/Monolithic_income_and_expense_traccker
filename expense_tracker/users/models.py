from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    source = models.CharField(max_length=255)  # Source of income (e.g., Salary, Bonus)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount
    date = models.DateField()  # Date of income

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    EXPENSE_TYPES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('utility', 'Utility'),
        ('entertainment', 'Entertainment'),
        ('others', 'Others'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    expense_type = models.CharField(max_length=50, choices=EXPENSE_TYPES)  # Type of expense
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount
    location = models.CharField(max_length=255)  # Location of expense
    date = models.DateField()  # Date of expense
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.expense_type} - {self.amount}"

class ExpenseCategoryLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user has one set of limits
    food_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transport_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    utility_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    entertainment_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    others_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Expense Limits for {self.user.username}"