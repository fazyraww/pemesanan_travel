from rest_framework import serializers
from .models import Perjalanan, Pemesanan, Ulasan

# --- 1. Serializer untuk Model Perjalanan (Trip) ---
class PerjalananSerializer(serializers.ModelSerializer):
    """Mengubah objek Perjalanan menjadi format JSON."""
    
    # Menambahkan field read-only untuk menampilkan jumlah ulasan
    jumlah_ulasan = serializers.SerializerMethodField() 
    
    class Meta:
        model = Perjalanan
        fields = ['id', 'tujuan', 'tgl_berangkat', 'tgl_kembali', 'harga', 'deskripsi', 'jumlah_ulasan']
        
    def get_jumlah_ulasan(self, obj):
        # Menghitung jumlah ulasan yang terkait dengan perjalanan ini
        return obj.ulasan.count()


# --- 2. Serializer untuk Model Pemesanan (Booking) ---
class PemesananSerializer(serializers.ModelSerializer):
    """Mengubah objek Pemesanan menjadi format JSON."""
    
    # Field ini hanya untuk input (write_only=True). 
    # API menerima ID perjalanan, tapi menyimpannya sebagai objek Perjalanan.
    perjalanan_id = serializers.PrimaryKeyRelatedField(
        queryset=Perjalanan.objects.all(), 
        source='perjalanan', 
        write_only=True
    )
    
    # Menampilkan nama tujuan saat data dibaca (read-only)
    nama_perjalanan = serializers.CharField(source='perjalanan.tujuan', read_only=True)

    class Meta:
        model = Pemesanan
        # total_harga dan tgl_pemesanan akan dihitung otomatis di save() model
        fields = [
            'id', 
            'perjalanan_id', 
            'nama_perjalanan', # Ditampilkan saat GET
            'nama_pelanggan', 
            'jumlah_orang', 
            'total_harga', 
            'tgl_pemesanan'
        ]
        # Field yang tidak boleh diubah oleh API pengguna
        read_only_fields = ['total_harga', 'tgl_pemesanan']


# --- 3. Serializer untuk Model Ulasan (Review) ---
class UlasanSerializer(serializers.ModelSerializer):
    """Mengubah objek Ulasan menjadi format JSON."""
    
    class Meta:
        model = Ulasan
        fields = '__all__'
        # tgl_dibuat diisi otomatis oleh model
        read_only_fields = ['tgl_dibuat']