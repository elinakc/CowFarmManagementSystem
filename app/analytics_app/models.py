from django.db import models
from app.animal_records.models import AnimalRecords

class MilkYieldPrediction(models.Model):
    cow = models.ForeignKey(AnimalRecords, on_delete=models.CASCADE)
    predicted_yield = models.FloatField()
    prediction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for {self.cow.cow_name} on {self.prediction_date}"