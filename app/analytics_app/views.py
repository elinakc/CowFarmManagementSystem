from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .metrics import AnimalAnalyticsService, MilkProductionAnalytics, HealthAnalytics, ComprehensiveAnalytics
from datetime import datetime
from app.milk_records.models import MilkRecord
from app.animal_records.models import AnimalRecords
from app.health_records.models import HealthRecord
# from .analytics_engine import AdvancedAnalyticsService

class FarmAnalyticsViewSet(ViewSet):
    @action(detail=False, methods=['GET'])
    def breeds(self, request):
        """Get breed analytics"""
        data = AnimalAnalyticsService.get_breed_analytics()
        return Response(data)

    @action(detail=False, methods=['GET'])
    def milk_production(self, request):
        """Get milk production analytics"""
        data = AnimalAnalyticsService.get_milk_production_analytics()
        return Response(data)

    @action(detail=False, methods=['GET'])
    def pregnancy(self, request):
        """Get pregnancy analytics"""
        data = AnimalAnalyticsService.get_pregnancy_analytics()
        return Response(data)

    @action(detail=False, methods=['GET'])
    def age(self, request):
        """Get age analytics"""
        data = AnimalAnalyticsService.get_age_analytics()
        return Response(data)

    @action(detail=False, methods=['GET'])
    def comprehensive_report(self, request):
        """Get comprehensive analytics report"""
        data = AnimalAnalyticsService.get_comprehensive_report()
        return Response(data)



class FarmAnalyticsViewSet(ViewSet):
    def get_date_range(self, request):
        """Helper method to get date range from request parameters"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
        return start_date, end_date

    @action(detail=False, methods=['GET'])
    def milk_production(self, request):
        """Get milk production analytics"""
        start_date, end_date = self.get_date_range(request)
        data = MilkProductionAnalytics.get_milk_production_insights(start_date, end_date)
        return Response(data)

    @action(detail=False, methods=['GET'])
    def health(self, request):
        """Get health analytics"""
        start_date, end_date = self.get_date_range(request)
        data = HealthAnalytics.get_health_insights(start_date, end_date)
        return Response(data)


    @action(detail=False, methods=['GET'])
    def comprehensive_report(self, request):
        """Get comprehensive farm analytics"""
        start_date, end_date = self.get_date_range(request)
        data = ComprehensiveAnalytics.get_farm_performance_metrics(start_date, end_date)
        return Response(data)
    


# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from .analytics_engine import (
#     StatisticalAnalytics,
#     PredictiveAnalytics,
#     ClusteringAnalytics,
#     AdvancedAnalyticsService
# )
# from .models import MilkRecord, HealthRecord
# from app.animal_records.models import AnimalRecords
# from django.shortcuts import get_object_or_404
# from datetime import datetime, timedelta

# @require_http_methods(["GET"])
# def milk_production_stats(request):
#     """View for milk production statistics"""
#     try:
#         # Get optional date range from query parameters
#         start_date = request.GET.get('start_date')
#         end_date = request.GET.get('end_date')
        
#         # Filter records based on date range if provided
#         milk_records = MilkRecord.objects.all()
#         if start_date:
#             milk_records = milk_records.filter(milking_date__gte=start_date)
#         if end_date:
#             milk_records = milk_records.filter(milking_date__lte=end_date)
            
#         stats = StatisticalAnalytics.calculate_milk_production_stats(milk_records)
#         return JsonResponse({
#             'status': 'success',
#             'data': stats
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)

# @require_http_methods(["GET"])
# def predict_milk_production(request):
#     """View for milk production predictions"""
#     try:
#         days = int(request.GET.get('days', 30))  # Default to 30 days
#         milk_records = MilkRecord.objects.all().order_by('milking_date')
        
#         predictions = PredictiveAnalytics.predict_milk_production(
#             milk_records,
#             days_to_predict=days
#         )
        
#         return JsonResponse({
#             'status': 'success',
#             'data': predictions
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)

# @require_http_methods(["GET"])
# def predict_health_risks(request):
#     """View for health risk predictions"""
#     try:
#         health_records = HealthRecord.objects.all()
#         animal_records =AnimalRecords.objects.all()
        
#         risks = PredictiveAnalytics.predict_health_risks(
#             health_records,
#             animal_records
#         )
        
#         return JsonResponse({
#             'status': 'success',
#             'data': risks
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)

# @require_http_methods(["GET"])
# def cluster_performance(request):
#     """View for clustering analysis"""
#     try:
#         animal_records = AnimalRecords.objects.all()
#         milk_records = MilkRecord.objects.all()
        
#         clusters = ClusteringAnalytics.cluster_animals_by_performance(
#             animal_records,
#             milk_records
#         )
        
#         return JsonResponse({
#             'status': 'success',
#             'data': clusters
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)

# @require_http_methods(["GET"])
# def advanced_analytics(request):
#     """View for comprehensive analytics"""
#     try:
#         milk_records = MilkRecord.objects.all()
#         health_records = HealthRecord.objects.all()
#         animal_records = AnimalRecords.objects.all()
        
#         analytics_service = AdvancedAnalyticsService(
#             milk_records,
#             health_records,
#             animal_records
#         )
        
#         results = analytics_service.generate_advanced_analytics()
        
#         return JsonResponse({
#             'status': 'success',
#             'data': results
#         })
#     except Exception as e:
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)