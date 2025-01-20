from django.db import models
from app.animal_records.models import AnimalRecords
# Create your models here.
class HealthRecord(models.Model):
  cow =models.ForeignKey(AnimalRecords, on_delete=models.CASCADE, related_name='health_records')
  health_condtion =models.CharField(max_length=255, choices=[
    ('healthy','Healthy'),
    ('sick','Sick'),
    ('undertreatment','Undertreatment'),
    
  ])
  diagnosed_illness =models.TextField(blank=True, null=True)
  vaccination_history =models.TextField(blank=True, null=True)
  veterinary_visits =models.TextField(blank=True, null=True)
  symptoms =models.TextField(blank=True, null=True)
  recovery_status =models.CharField(max_length=255, choices=[
    ('improving','Improving'),
    ('stable',"Stable"),
    ('worsening','Worsening'),
  ])
  treatment_cost =models.DecimalField(max_digits=10 , decimal_places=2)
  created_at =models.DateTimeField(auto_now_add=True)
  updated_at =models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"Health Record for {self.cow.name}"
  
  