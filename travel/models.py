from django.db import models
from django.db.models import Avg


class Perjalanan(models.Model):
    """Model yang merepresentasikan satu paket perjalanan (Trip)."""
    tujuan = models.CharField(max_length=100)
    deskripsi = models.TextField()
    tgl_berangkat = models.DateField()
    tgl_kembali = models.DateField()
    harga = models.DecimalField(max_digits=10, decimal_places=0) # Harga per orang

    def __str__(self):
        return f"Perjalanan ke {self.tujuan} ({self.tgl_berangkat})"
    
    @property
    def avg_rating(self):
        # Menggunakan related_name='ulasan'
        if self.ulasan.exists():
            return self.ulasan.aggregate(Avg('rating'))['rating__avg']
        return 0

class Pemesanan(models.Model):
    """Model untuk mencatat pemesanan yang dilakukan pelanggan."""
    # Relasi ForeignKey ke Perjalanan
    perjalanan = models.ForeignKey(Perjalanan, on_delete=models.CASCADE, related_name='pemesanan')
    nama_pelanggan = models.CharField(max_length=100)
    jumlah_orang = models.IntegerField()
    tgl_pemesanan = models.DateTimeField(auto_now_add=True)
    total_harga = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"Pemesanan oleh {self.nama_pelanggan} untuk {self.perjalanan.tujuan}"

    def save(self, *args, **kwargs):
        # Hitung total harga sebelum disimpan
        self.total_harga = self.jumlah_orang * self.perjalanan.harga
        super().save(*args, **kwargs)


class Ulasan(models.Model):
    """Model untuk ulasan dan rating sebuah perjalanan."""
    # Relasi ForeignKey ke Perjalanan
    perjalanan = models.ForeignKey(Perjalanan, on_delete=models.CASCADE, related_name='ulasan')
    nama_pengulas = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # Rating 1 sampai 5
    komentar = models.TextField(blank=True, null=True)
    tgl_ulasan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ulasan {self.rating}/5 untuk {self.perjalanan.tujuan}"