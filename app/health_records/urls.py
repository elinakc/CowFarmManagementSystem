from .import views
from django.urls import path, include
from .views import HealthRecordDetailView, HealthRecordListCreateView

urlpatterns = [
   
  path("health-records/", HealthRecordListCreateView.as_view(), name="health-record-list"),
  path("health-records/<int:pk>/", HealthRecordDetailView.as_view(), name="health-record-detail"),
]
