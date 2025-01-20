from rest_framework import serializers
from .models import HealthRecord
from app.animal_records.serializers import AnimalRecordsSerializer

class HealthRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = HealthRecord
    fields = "__all__" 
    
    
    

    
 

