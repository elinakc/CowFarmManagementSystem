from django.db import models
from django.utils import timezone
from app.animal_records.models import AnimalRecords
from app.milk_records.models import MilkRecord
from app.health_records.models import HealthRecord
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
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50, blank=True)
    
    milk_record = models.ForeignKey(
        MilkRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='milk_income_entries'
    )
    animal = models.ForeignKey(
        AnimalRecords,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='animal_income_entries'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

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
    description = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50, blank=True)
    
    health_record = models.ForeignKey(
        HealthRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='health_expense_entries'
    )
    animal = models.ForeignKey(
        AnimalRecords,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='animal_expense_entries'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.get_expense_type_display()} - {self.amount} on {self.date}"