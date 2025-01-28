from rest_framework import serializers
from .models import HealthRecord
from app.animal_records.models import AnimalRecords

class CowDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalRecords
        fields = ['id','cow_name'] 

class HealthRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = HealthRecord
    fields = "__all__" 
  
  def get_cow_options(self, obj):
        # Retrieve all cows for dropdown
        cows = AnimalRecords.objects.all()
        return CowDropdownSerializer(cows, many=True).data
    
    
    

    
 

