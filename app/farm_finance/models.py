from django.db import models
from django.utils import timezone
from django.conf import settings

class Income(models.Model):
    INCOME_TYPES = [
        ('MILK', 'Milk Sales'),
        ('CATTLE', 'Cattle Sales'),
        ('MANURE', 'Manure Sales'),
        ('OTHER', 'Other Income')
    ]
    
    date = models.DateField(default=timezone.now)
    income_type = models.CharField(
        max_length=20, 
        choices=INCOME_TYPES,
        default='OTHER'  # Added default
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
 
    def __str__(self):
        return f"{self.get_income_type_display()} - {self.amount} on {self.date}"
    

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('FEED', 'Feed Purchase'),
        ('VET', 'Veterinary Services'),
        ('LABOR', 'Labor Costs'),
        ('EQUIPMENT', 'Equipment'),
        ('MAINTENANCE', 'Maintenance'),
        ('OTHER', 'Other Expenses')
    ]
    
    date = models.DateField(default=timezone.now)
    expense_type = models.CharField(
        max_length=20, 
        choices=EXPENSE_TYPES,
        default='OTHER'  # Added default value
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
 
    
    def __str__(self):
        return f"{self.get_expense_type_display()} - {self.amount} on {self.date}"
