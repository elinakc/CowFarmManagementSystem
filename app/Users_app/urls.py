from .import views
from django.urls import path, include
from rest_framework.routers  import DefaultRouter
from .views import UserRegistrationView, LoginView, LogoutView, AdminDashboardView, VeterinarianDashboardView, ManagerDashboardView

router =DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',  LogoutView.as_view(), name='login'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('dashboard/vets/', VeterinarianDashboardView.as_view(), name='veterinarian-dashboard'),
    path('dashboard/manager/', ManagerDashboardView.as_view(), name='manager-dashboard'),
   
]