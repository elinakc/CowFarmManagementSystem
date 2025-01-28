from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import MilkRecord
from .serializers import MilkRecordSerializer, MonthlyMilkYieldSerializer,ProfitLossSerializer
from rest_framework.views import APIView
import logging
from .serializers import CowDropdownSerializer
from app.animal_records.models import AnimalRecords
from rest_framework import generics
from app.Users_app.permissions import role_required, IsAdmin, IsManager
from django.db.models import Sum, F, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth
from rest_framework.permissions import AllowAny
from django.utils.timezone import make_aware
from datetime import datetime, date


logger = logging.getLogger(__name__)

# @role_required(['admin','manager']) 
class CowListView(generics.ListAPIView):
    permission_classes = [AllowAny]    
    queryset = AnimalRecords.objects.all()
    serializer_class =CowDropdownSerializer


class MilkRecordListCreateView(APIView):
    permission_classes = [AllowAny]
    # @role_required(['admin','manager']) 
    
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
            
    
    # @role_required(['admin','manager']) 
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
    permission_classes = [AllowAny]
    # @role_required(['admin','manager']) 
   
   
    def get_object(self, pk):
        try:
            return MilkRecord.objects.get(pk=pk)
        except MilkRecord.DoesNotExist:
            return None
        
    
    # @role_required(['admin','manager']) 
    def get(self, request, pk):
        """Retrieve a specific milk record"""
        milk_record = self.get_object(pk=pk)
        if milk_record:
            serializer = MilkRecordSerializer(milk_record)
            return Response(serializer.data)
        return Response(
            {"error": "Milk record not found"}, status=status.HTTP_404_NOT_FOUND
        )
  
    
    # @role_required(['admin','manager'])  
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
        
   
    # @role_required(['admin','manager']) 
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
        
class MonthlyMilkYieldView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        monthly_yields = MilkRecord.objects.annotate(
            month=TruncMonth('milking_date')
        ).values('month').annotate(
            total_morning_milk=Sum('morning_milk_quantity'),
            total_afternoon_milk=Sum('afternoon_milk_quantity'),
            total_evening_milk=Sum('evening_milk_quantity'),
            total_daily_milk=Sum('morning_milk_quantity') + 
                              Sum('afternoon_milk_quantity') + 
                              Sum('evening_milk_quantity')
        ).order_by('-month')
        for record in monthly_yields:
            if isinstance(record['month'], datetime):
                # If it's already a datetime, just make it timezone aware
                record['month'] = make_aware(record['month'])
            elif isinstance(record['month'], date):
                # If it's a date object, convert to datetime first
                record['month'] = make_aware(datetime.combine(record['month'], datetime.min.time()))
                
        serializer = MonthlyMilkYieldSerializer(monthly_yields, many=True)
        return Response(serializer.data)
    
class ProfitLossCalculationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Calculate monthly profit/loss based on milk yield"""
        # Assuming following cost/revenue parameters (you should adjust these)
        MILK_PRICE_PER_LITER = 50  # Price per liter of milk
        FEED_COST_PER_COW_PER_MONTH = 5000  # Monthly feed cost per cow
        MAINTENANCE_COST_PER_COW_PER_MONTH = 2000  # Monthly maintenance cost per cow
        
        # Get monthly milk yields
        monthly_yields = MilkRecord.objects.annotate(
            month=TruncMonth('milking_date')
        ).values('month').annotate(
            total_monthly_milk=Sum(
                F('morning_milk_quantity') + 
                F('afternoon_milk_quantity') + 
                F('evening_milk_quantity')
            ),
            total_cows=Count('cow', distinct=True)
        ).order_by('-month')
        for record in monthly_yields:
            if isinstance(record['month'], datetime):
                # If it's already a datetime, just make it timezone aware
                record['month'] = make_aware(record['month'])
            elif isinstance(record['month'], date):
                # If it's a date object, convert to datetime first
                record['month'] = make_aware(datetime.combine(record['month'], datetime.min.time()))
        
        profit_loss_data = []
        for monthly_data in monthly_yields:
            total_milk_revenue = monthly_data['total_monthly_milk'] * MILK_PRICE_PER_LITER
            total_feed_cost = monthly_data['total_cows'] * FEED_COST_PER_COW_PER_MONTH
            total_maintenance_cost = monthly_data['total_cows'] * MAINTENANCE_COST_PER_COW_PER_MONTH
            
            profit_loss = total_milk_revenue - total_feed_cost - total_maintenance_cost
            
            profit_loss_data.append({
                'month': monthly_data['month'],
                'total_milk_quantity': monthly_data['total_monthly_milk'],
                'total_milk_revenue': total_milk_revenue,
                'total_feed_cost': total_feed_cost,
                'total_maintenance_cost': total_maintenance_cost,
                'net_profit_loss': profit_loss
            })
        
        serializer = ProfitLossSerializer(profit_loss_data, many=True)
        return Response(serializer.data)