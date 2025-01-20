from django.contrib import admin
from django.urls import path, include

from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/", include('app.Users_app.urls')),
    path("api/", include('app.animal_records.urls')),
    path("api/", include('app.milk_records.urls')),
    path("api/", include('app.health_records.urls')),
    path("api/", include('app.farm_finance.urls')),
    path('api/', include('app.analytics_app.urls')),
   
    

]
