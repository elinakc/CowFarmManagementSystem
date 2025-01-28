from .models import MilkRecord
from app.animal_records.models import AnimalRecords
from rest_framework import serializers

class CowDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalRecords
        fields = ['id','cow_name'] 
  
class MilkRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = MilkRecord
    fields =['id','cow', 'milking_date', 'morning_milk_quantity','afternoon_milk_quantity','evening_milk_quantity']
    extra_fields = ['total_milk_quantity']  # Add dynamic field
    
  def get_cow_options(self, obj):
        # Retrieve all cows for dropdown
        cows = AnimalRecords.objects.all()
        return CowDropdownSerializer(cows, many=True).data

  def get_total_milk_quantity(self, obj):
        """Calculate total milk quantity for the record."""
        return (
              obj.morning_milk_quantity +
              obj.afternoon_milk_quantity +
              obj.evening_milk_quantity
          )
        

class MonthlyMilkYieldSerializer(serializers.Serializer):
    
    month = serializers.DateTimeField()
    total_morning_milk = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_afternoon_milk = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_evening_milk = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_daily_milk = serializers.DecimalField(max_digits=10, decimal_places=2)
    
  

class ProfitLossSerializer(serializers.Serializer):
    month = serializers.DateTimeField()
    total_milk_quantity = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_milk_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_feed_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_maintenance_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_profit_loss = serializers.DecimalField(max_digits=10, decimal_places=2)