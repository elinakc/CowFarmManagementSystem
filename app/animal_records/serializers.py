from .models import AnimalRecords
from rest_framework import serializers

class AnimalRecordsSerializer(serializers.ModelSerializer):
  class Meta:
    model = AnimalRecords
    fields = "__all__"
  