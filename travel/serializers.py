from rest_framework import serializers
from .models import Perjalanan, Pemesanan, Ulasan

class PerjalananSerializer(serializers.ModelSerializer):
    """Serializer untuk model Perjalanan (Paket Travel)"""
    class Meta:
        model = Perjalanan
        fields = '__all__' # Sertakan semua field dari model Perjalanan

class PemesananSerializer(serializers.ModelSerializer):
    """Serializer untuk model Pemesanan"""
    class Meta:
        model = Pemesanan
        # Sertakan semua field, termasuk perjalanan (ForeignKey)
        fields = '__all__'

class UlasanSerializer(serializers.ModelSerializer):
    """Serializer untuk model Ulasan"""
    class Meta:
        model = Ulasan
        # Sertakan semua field
        fields = '__all__'