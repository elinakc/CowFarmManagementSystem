from django.db import models
from datetime import date 
from app.animal_records.models import AnimalRecords
# Create your models here.
class MilkRecord(models.Model):
  milking_date =models.DateField(default=date.today)
  cow = models.ForeignKey(AnimalRecords, on_delete=models.CASCADE,related_name='milk_records')
  morning_milk_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  afternoon_milk_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
  evening_milk_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
 
  def total_milk_quantity(self):
    return self.morning_milk_quantity + self.afternoon_milk_quantity + self.evening_milk_quantity
  
  def __str__(self):
    return f"Milk Record for {self.cow.name or self.cow_id} on {self.milking_date}"
  
    