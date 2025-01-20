from rest_framework import serializers
from .models import Income, Expense
from app.milk_records.serializers import MilkRecordSerializer
from app.animal_records.serializers import AnimalRecordsSerializer
from app.health_records.serializers import HealthRecordSerializer

class IncomeSerializer(serializers.ModelSerializer):
    milk_record_details = MilkRecordSerializer(source='milk_record', read_only=True)
    animal_details = AnimalRecordsSerializer(source='animal', read_only=True)

    class Meta:
        model = Income
        fields = ['id', 'date', 'income_type', 'description', 'amount', 
                 'reference_number', 'milk_record', 'animal', 'milk_record_details',
                 'animal_details','created_by']
        read_only_fields = ['created_by']
        

class ExpenseSerializer(serializers.ModelSerializer):
    health_record_details = HealthRecordSerializer(source='health_record', read_only=True)
    animal_details = AnimalRecordsSerializer(source='animal', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'date', 'expense_type', 'description', 'amount',
                 'reference_number', 'health_record', 'animal', 'health_record_details',
                 'animal_details','created_by']
        read_only_fields = ['created_by'] 
        
        
       