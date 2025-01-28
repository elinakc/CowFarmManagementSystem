from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class AnimalRecords(models.Model):
  cow_name = models.CharField(max_length=255, blank=True, null=True)
  breed = models.CharField(max_length=255)
  dob =models.DateField()
  date_of_arrival =models.DateField()
  weight = models.DecimalField(max_digits=5, decimal_places=2)
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
    return self.cow_name
  
  

  
  def clean(self):
    today = timezone.now().date()
    # Validate date of birth is not in the future
    if self.dob and self.dob > timezone.now().date():
        raise ValidationError({
            'dob': 'Date of birth cannot be in the future.'
        })

    # Validate date of arrival is not before date of birth
    if self.dob and self.date_of_arrival and self.date_of_arrival < self.dob:
        raise ValidationError({
            'date_of_arrival': 'Date of arrival cannot be before date of birth.'
        })
        
    if self.date_of_arrival and self.date_of_arrival > today:
      raise ValidationError('Date of arrival cannot be in the future')    

    # Validate due date only required when pregnancy status is true
    if self.pregnancy_status and not self.due_date:
        raise ValidationError({
            'due_date': 'Due date is required when pregnancy status is true.'
        })

    # Validate due date is not in the past when pregnancy status is true
    if self.pregnancy_status and self.due_date and self.due_date < timezone.now().date():
        raise ValidationError({
            'due_date': 'Due date cannot be in the past when pregnant.'
        })

def save(self, *args, **kwargs):
    self.full_clean()
    return super().save(*args, **kwargs)
  


