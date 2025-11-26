from django.contrib import admin
from .models import Perjalanan, Pemesanan, Ulasan # Tambahkan Ulasan

# 1. Konfigurasi Model Perjalanan (Trip)
@admin.register(Perjalanan)
class PerjalananAdmin(admin.ModelAdmin):
    # Menampilkan field utama di daftar tabel admin
    list_display = ('tujuan', 'tgl_berangkat', 'tgl_kembali', 'harga')
    # Memungkinkan pencarian berdasarkan field tujuan
    search_fields = ('tujuan',)
    # Field yang bisa diedit langsung dari daftar tabel
    list_editable = ('harga',)

# 2. Konfigurasi Model Pemesanan (Booking)
@admin.register(Pemesanan)
class PemesananAdmin(admin.ModelAdmin):
    # Menampilkan field utama dan hasil perhitungan
    list_display = ('nama_pelanggan', 'perjalanan', 'jumlah_orang', 'total_harga', 'tgl_pemesanan')
    # Filter data berdasarkan perjalanan dan tanggal pemesanan
    list_filter = ('perjalanan', 'tgl_pemesanan')
    # Field yang tidak bisa diubah (karena dihitung otomatis)
    readonly_fields = ('total_harga', 'tgl_pemesanan')

# 3. Konfigurasi Model Ulasan (Review) - Opsional, tapi disarankan
@admin.register(Ulasan)
class UlasanAdmin(admin.ModelAdmin):
    list_display = ('perjalanan', 'rating', 'nama_pengulas', 'tgl_ulasan')
    list_filter = ('perjalanan', 'rating')
    search_fields = ('komentar', 'nama_pengulas')