from django.db import models

# Create your models here.
class AnimalRecords(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  breed = models.CharField(max_length=255)
  dob =models.DateField()
  date_of_arrival =models.DateField()
  weight = models.DecimalField(max_digits=5, decimal_places=2)
  daily_milk_yield = models.DecimalField(max_digits=5 , decimal_places=2, blank=True, null=True)
  monthly_milk_yield = models.DecimalField(max_digits=5 , decimal_places=2, blank=True, null=True)
  pregnancy_status = models.BooleanField(default=False)
  due_date = models.DateField(blank=True, null=True)
  lactation_cycle = models.CharField(max_length=50, choices=[
        ('dry', 'Dry'),
        ('lactating', 'Lactating'),
        ('fresh', 'Fresh')
    ])
  health_history = models.TextField(blank=True, null=True)
  breeding_history =models.TextField(blank=True, null=True)
  
  def __str__(self):
    return self.name
  
  

  
  