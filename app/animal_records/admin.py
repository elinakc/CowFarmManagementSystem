from django.contrib import admin
from .models import AnimalRecords
# Register your models here.
class AnimalRecordsAdmin(admin.ModelAdmin):
  list_display=['id','name','breed','date_of_arrival']
  
admin.site.register(AnimalRecords , AnimalRecordsAdmin)