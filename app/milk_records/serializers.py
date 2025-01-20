from .models import MilkRecord
from rest_framework import serializers


class MilkRecordSerializer(serializers.ModelSerializer):
  class Meta:
    model = MilkRecord
    fields =['cow', 'milking_date', 'morning_milk_quantity','afternoon_milk_quantity','evening_milk_quantity']
    extra_fields = ['total_milk_quantity']  # Add dynamic field

  def get_total_milk_quantity(self, obj):
        """Calculate total milk quantity for the record."""
        return (
              obj.morning_milk_quantity +
              obj.afternoon_milk_quantity +
              obj.evening_milk_quantity
          )