from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rute untuk Web Views
    path('travel/', include('travel.urls')), 
    
    # Rute untuk API, menunjuk ke file API yang baru
    path('api/', include('travel.api_urls')), 
]