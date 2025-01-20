from .import views
from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from .views import CreateAnimalView, AnimalDetailView, AnimalListView

router =DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('animal/', AnimalListView.as_view(), name='animal-list'),
    path('animal/create', CreateAnimalView.as_view(), name='animal-create'),
    path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
  
]