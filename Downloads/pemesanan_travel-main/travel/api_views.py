from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Perjalanan, Pemesanan
from .serializers import PerjalananSerializer, PemesananSerializer

class PerjalananViewSet(viewsets.ModelViewSet):
    """ViewSet untuk mengelola endpoint CRUD Perjalanan."""
    queryset = Perjalanan.objects.all().order_by('tgl_berangkat')
    serializer_class = PerjalananSerializer
    permission_classes = [AllowAny] 

class PemesananViewSet(viewsets.ModelViewSet):
    """ViewSet untuk mengelola endpoint CRUD Pemesanan."""
    queryset = Pemesanan.objects.all().order_by('-tgl_pemesanan')
    serializer_class = PemesananSerializer
    permission_classes = [AllowAny]