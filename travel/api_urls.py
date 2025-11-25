from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PerjalananViewSet, PemesananViewSet, UlasanViewSet

# Menggunakan DefaultRouter dari DRF
router = DefaultRouter()
# 1. Rute untuk Model Perjalanan
router.register(r'perjalanan', PerjalananViewSet, basename='perjalanan-api')
# 2. Rute untuk Model Pemesanan
router.register(r'pemesanan', PemesananViewSet, basename='pemesanan-api')
# 3. Rute untuk Model Ulasan
router.register(r'ulasan', UlasanViewSet, basename='ulasan-api')

# Daftar URL API
urlpatterns = [
    # Semua rute yang dibuat oleh router akan disertakan di sini.
    # Misalnya, GET /api/v1/perjalanan/ atau POST /api/v1/pemesanan/
    path('v1/', include(router.urls)),
]