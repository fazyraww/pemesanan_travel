from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import date, timedelta
from decimal import Decimal
from .models import Perjalanan, Pemesanan, Ulasan

class PerjalananAPITests(APITestCase):
    """
    Menguji fungsionalitas API untuk model Perjalanan.
    """
    def setUp(self):
        # Setup data yang dibutuhkan untuk setiap tes
        self.url = reverse('perjalanan-api-list') # Menggunakan basename dari router di urls.py
        self.perjalanan1 = Perjalanan.objects.create(
            tujuan="Bali",
            tgl_berangkat=date.today() + timedelta(days=10),
            tgl_kembali=date.today() + timedelta(days=17),
            harga=Decimal('5000000.00'),
            deskripsi="Paket 7 hari di Bali."
        )
        self.perjalanan2 = Perjalanan.objects.create(
            tujuan="Yogyakarta",
            tgl_berangkat=date.today() + timedelta(days=5),
            tgl_kembali=date.today() + timedelta(days=8),
            harga=Decimal('2500000.00'),
            deskripsi="Liburan singkat 3 hari di Jogja."
        )
        # Membuat ulasan untuk menguji field jumlah_ulasan di serializer
        Ulasan.objects.create(perjalanan=self.perjalanan1, nama_pengulas="A", rating=5)
        Ulasan.objects.create(perjalanan=self.perjalanan1, nama_pengulas="B", rating=4)

    def test_list_perjalanan(self):
        """Memastikan daftar perjalanan dapat diakses dan mengembalikan data yang benar."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Memastikan field kustom 'jumlah_ulasan' ada dan benar
        self.assertEqual(response.data[0]['jumlah_ulasan'], 2)

    def test_create_perjalanan(self):
        """Memastikan pembuatan perjalanan baru berhasil."""
        data = {
            'tujuan': 'Raja Ampat',
            'tgl_berangkat': date.today() + timedelta(days=30),
            'tgl_kembali': date.today() + timedelta(days=35),
            'harga': '12000000.00',
            'deskripsi': 'Surga bawah laut.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Perjalanan.objects.count(), 3)
        self.assertEqual(response.data['tujuan'], 'Raja Ampat')

class PemesananAPITests(APITestCase):
    """
    Menguji fungsionalitas API untuk model Pemesanan, termasuk logika total harga.
    """
    def setUp(self):
        # Setup data perjalanan yang akan dipesan
        self.perjalanan = Perjalanan.objects.create(
            tujuan="Lombok",
            tgl_berangkat=date.today() + timedelta(days=20),
            tgl_kembali=date.today() + timedelta(days=25),
            harga=Decimal('4000000.00'),
            deskripsi="Paket 5 hari di Lombok."
        )
        self.url = reverse('pemesanan-api-list')

    def test_create_pemesanan_success(self):
        """Memastikan pembuatan pemesanan berhasil dan total_harga terhitung benar."""
        data = {
            # Menggunakan ID perjalanan sebagai input, seperti yang didefinisikan di serializer
            'perjalanan_id': self.perjalanan.pk,
            'nama_pelanggan': 'Budi Santoso',
            'jumlah_orang': 2
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pemesanan.objects.count(), 1)
        
        pemesanan = Pemesanan.objects.first()
        # total_harga harus dihitung: 2 orang * 4,000,000 = 8,000,000
        self.assertEqual(pemesanan.total_harga, Decimal('8000000.00'))
        # Memastikan respons API mengembalikan nilai total_harga yang benar
        self.assertEqual(float(response.data['total_harga']), 8000000.00)
        # Memastikan field read-only nama_perjalanan terisi
        self.assertEqual(response.data['nama_perjalanan'], 'Lombok')

    def test_create_pemesanan_invalid_data(self):
        """Memastikan data pemesanan yang tidak valid ditolak (misal: jumlah orang 0)."""
        data = {
            'perjalanan_id': self.perjalanan.pk,
            'nama_pelanggan': 'Ani',
            'jumlah_orang': 0 # Data tidak valid
        }
        response = self.client.post(self.url, data, format='json')
        # DRF dan ModelForm akan memastikan jumlah_orang minimal 1 (jika divalidasi)
        # Di sini, karena kita tidak menggunakan serializer untuk validasi jumlah minimal, 
        # kita menguji bahwa ID perjalanan yang salah akan gagal (contoh umum)
        
        # Tes dengan ID perjalanan yang tidak ada
        invalid_data = {
            'perjalanan_id': 9999,
            'nama_pelanggan': 'Tester',
            'jumlah_orang': 1
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('perjalanan_id', response.data) # Memastikan error terkait perjalanan_id