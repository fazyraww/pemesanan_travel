from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PerjalananViewSet, PemesananViewSet 

# Router untuk API DRF
router = DefaultRouter()
router.register(r'perjalanan', PerjalananViewSet, basename='perjalanan-api')
router.register(r'pemesanan', PemesananViewSet, basename='pemesanan-api')

# Variabel WAJIB yang DITERUSKAN ke Django
urlpatterns = [
    path('', include(router.urls)), 
]