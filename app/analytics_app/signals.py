from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from app.animal_records.models import AnimalRecords
from app.milk_records.models import MilkRecord
from .ml_models import MilkYieldPredictor

@receiver(post_save, sender=AnimalRecords)
@receiver(post_save, sender=MilkRecord)
@receiver(post_delete, sender=AnimalRecords)
@receiver(post_delete, sender=MilkRecord)
def retrain_model(sender, instance, **kwargs):
    print("Data updated! Retraining the model...")
    predictor = MilkYieldPredictor()
    predictor.train_model()
    print("Model retrained successfully!")
