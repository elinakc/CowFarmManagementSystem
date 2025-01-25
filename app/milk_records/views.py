from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import MilkRecord
from .serializers import MilkRecordSerializer
from rest_framework.views import APIView
from rest_framework import  permissions, status
import logging
from .serializers import CowDropdownSerializer
from app.animal_records.models import AnimalRecords
from rest_framework import generics
from app.Users_app.permissions import role_required, IsAdmin, IsManager


logger = logging.getLogger(__name__)

@role_required(['admin','manager']) 
class CowListView(generics.ListAPIView):
    # permission_classes = [IsAdmin | IsManager]    
    queryset = AnimalRecords.objects.all()
    serializer_class =CowDropdownSerializer


class MilkRecordListCreateView(APIView):
    permission_classes = [IsAdmin | IsManager]
    @role_required(['admin','manager']) 
    
    def get(self, request):
        """Get all milk records"""
        try:
            milk_records = MilkRecord.objects.all().order_by('-milking_date')
            serializer = MilkRecordSerializer(milk_records, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching milk records: {str(e)}")
            return Response(
                {"error": "Failed to fetch milk records"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    
    @role_required(['admin','manager']) 
    def post(self, request):
        """Create a new milk record"""
        logger.info(f"Received data: {request.data}")
        
        # Convert empty strings to None for number fields
        data = request.data.copy()
        number_fields = ['morningMilkQuantity', 'afternoonMilkQuantity', 'eveningMilkQuantity']
        for field in number_fields:
            if field in data and data[field] == '':
                data[field] = None

        # Check if a record for the same cow and date already exists
        existing_record = MilkRecord.objects.filter(
            cow_id=data.get('cow'),
            milking_date=data.get('milking_date')
        ).exists()

        if existing_record:
            return Response(
                {"error": "A milk record for this cow on this date already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MilkRecordSerializer(data=data)
        if serializer.is_valid():
            logger.info("Data is valid")
            serializer.save()
            logger.info("Data saved successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilkRecordDetailView(APIView):
    permission_classes = [IsAdmin | IsManager]
    @role_required(['admin','manager']) 
   
   
    def get_object(self, pk):
        try:
            return MilkRecord.objects.get(pk=pk)
        except MilkRecord.DoesNotExist:
            return None
        
    
    @role_required(['admin','manager']) 
    def get(self, request, pk):
        """Retrieve a specific milk record"""
        milk_record = self.get_object(pk=pk)
        if milk_record:
            serializer = MilkRecordSerializer(milk_record)
            return Response(serializer.data)
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
  
    
    @role_required(['admin','manager'])  
    def put(self, request, pk):
        """Update a specific milk record"""
        milk_record = self.get_object(pk=pk)
        if milk_record:
            serializer = MilkRecordSerializer(
                milk_record, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
        
   
    @role_required(['admin','manager']) 
    def delete(self, request, pk):
        """Delete a specific milk record"""
        milk_record = self.get_object(pk=pk)
        if milk_record:
            milk_record.delete()
            return Response(
                {"message": "Milk record deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
