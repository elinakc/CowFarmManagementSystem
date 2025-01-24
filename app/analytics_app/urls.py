from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmAnalyticsViewSet 
# milk_production_stats, predict_milk_production,cluster_performance,advanced_analytics


router = DefaultRouter()
router.register(r'analytics', FarmAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    #  # Statistical Analytics endpoints
    # path('stats/milk-production/', views.milk_production_stats, name='milk_production_stats'),
    
    # # Predictive Analytics endpoints
    # path('predict/milk-production/', views.predict_milk_production, name='predict_milk_production'),
    # path('predict/health-risks/', views.predict_health_risks, name='predict_health_risks'),
    
    # # Clustering Analytics endpoints
    # path('cluster/performance/', views.cluster_performance, name='cluster_performance'),
    
    # # Combined Analytics endpoint
    # path('advanced-analytics/', views.advanced_analytics, name='advanced_analytics'),
]
