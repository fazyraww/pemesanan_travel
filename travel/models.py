from django.db import models

class Perjalanan(models.Model): # Tabel 1: Perjalanan
    """Model untuk mendefinisikan paket perjalanan yang tersedia."""
    
    TGL_CHOICES = [
        (1, 'Sangat Buruk'), (2, 'Buruk'), (3, 'Cukup'), (4, 'Bagus'), (5, 'Sangat Bagus')
    ]

    tujuan = models.CharField(max_length=200, verbose_name="Tujuan Destinasi")
    tgl_berangkat = models.DateField(verbose_name="Tanggal Keberangkatan")
    tgl_kembali = models.DateField(verbose_name="Tanggal Kembali")
    harga = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga per Orang")
    deskripsi = models.TextField(blank=True, verbose_name="Deskripsi Paket")
    
    class Meta:
        verbose_name = "Perjalanan"
        verbose_name_plural = "Daftar Perjalanan"

    def __str__(self): 
        return f"Perjalanan ke {self.tujuan}"

class Pemesanan(models.Model): # Tabel 2: Pemesanan
    """Model untuk menyimpan detail pemesanan oleh pelanggan."""
    
    perjalanan = models.ForeignKey(Perjalanan, on_delete=models.CASCADE, related_name='pemesanan', verbose_name="Paket Perjalanan")
    nama_pelanggan = models.CharField(max_length=100, verbose_name="Nama Pelanggan")
    jumlah_orang = models.IntegerField(default=1, verbose_name="Jumlah Orang Dipesan")
    tgl_pemesanan = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Pemesanan")
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Total Harga")
    
    class Meta:
        verbose_name = "Pemesanan"
        verbose_name_plural = "Daftar Pemesanan"

    def save(self, *args, **kwargs):
        # Otomatis menghitung total harga
        self.total_harga = self.jumlah_orang * self.perjalanan.harga
        super().save(*args, **kwargs)
        
    def __str__(self): 
        return f"Pemesanan oleh {self.nama_pelanggan} ({self.perjalanan.tujuan})"
        
class Ulasan(models.Model): # Tabel 3: Ulasan
    """Model untuk menyimpan ulasan dan rating untuk setiap perjalanan."""
    
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    perjalanan = models.ForeignKey(Perjalanan, on_delete=models.CASCADE, related_name='ulasan', verbose_name="Perjalanan yang Diulas")
    nama_pengulas = models.CharField(max_length=100, verbose_name="Nama Pengulas")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Rating (1-5)")
    komentar = models.TextField(blank=True, verbose_name="Komentar Ulasan")
    tgl_dibuat = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Dibuat")
    
    class Meta:
        verbose_name = "Ulasan"
        verbose_name_plural = "Daftar Ulasan"

    def __str__(self): 
        return f"Ulasan untuk {self.perjalanan.tujuan} ({self.rating}/5)"