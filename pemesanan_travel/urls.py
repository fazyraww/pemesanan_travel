"""
URL configuration for pemesanan_travel project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rute untuk Web View (Hanya merujuk ke path tanpa prefix 'api/v1/')
    # Endpoint: /travel/
    path('travel/', include(([
        path('', views.daftar_perjalanan, name='daftar_perjalanan')
    ], 'travel'), namespace='travel_web')), 

    # 2. Rute untuk API (Hanya merujuk ke path dengan prefix 'api/v1/')
    # Endpoint: /api/v1/perjalanan/
    path('api/', include('travel.urls')), # Di sini kita taruh semua routing API
]