from .models import AnimalRecords
from rest_framework import serializers
from datetime import date, timezone
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date

# from django.core.exceptions import ValidationError
from django.utils.timezone import now
class AnimalRecordsSerializer(serializers.ModelSerializer):
  pregnancy_status = serializers.BooleanField(default=False)
  due_date = serializers.DateField(required=False, allow_null=True)
  class Meta:
    model = AnimalRecords
    fields = "__all__"
    
    def validate_due_date(self, value):
        if value:
            # Ensure date is valid and in correct format
            try:
                # Convert to date object
                parsed_date = timezone.datetime.strptime(str(value), '%Y-%m-%d').date()
                return parsed_date
            except ValueError:
                raise serializers.ValidationError("Invalid date format. Use YYYY-MM-DD")
            
 