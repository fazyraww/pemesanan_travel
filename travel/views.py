from django.http import JsonResponse
from .models import Perjalanan  # Pastikan model ada

# Fungsi untuk web view (sudah ada)
def daftar_perjalanan(request):
    # Kode Anda yang sudah ada, misalnya render template
    pass

# Tambahkan ini untuk API
def daftar_perjalanan_api(request):
    perjalanan_list = Perjalanan.objects.all().values('id', 'nama', 'harga')  # Sesuaikan field model
    return JsonResponse(list(perjalanan_list), safe=False)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Pastikan mengimpor model yang benar (Perjalanan, Pemesanan, Ulasan)
from .models import Perjalanan, Pemesanan, Ulasan 
from .forms import PemesananForm # Pastikan forms.py sudah diimpor

# Tampilan 1: Menampilkan Daftar Semua Perjalanan (Menggantikan trip_list)
def daftar_perjalanan(request):
    """Tampilkan daftar semua perjalanan yang tersedia di trip_list.html."""
    # Menggunakan model Perjalanan dan mengurutkan berdasarkan tanggal berangkat
    semua_perjalanan = Perjalanan.objects.all().order_by('tgl_berangkat') 
    context = {'perjalanan_list': semua_perjalanan}
    return render(request, 'travel/trip_list.html', context)

# Tampilan 2: Menampilkan Detail Satu Perjalanan
def trip_detail(request, pk):
    """Menampilkan detail perjalanan tertentu berdasarkan primary key (pk)."""
    # Menggunakan get_object_or_404 untuk menampilkan 404 jika ID tidak ditemukan
    perjalanan = get_object_or_404(Perjalanan, pk=pk)
    context = {'perjalanan': perjalanan}
    return render(request, 'travel/trip_detail.html', context)

# Tampilan 3: Membuat Pemesanan Baru
def booking_create(request, pk):
    """Menangani logika untuk formulir pemesanan."""
    perjalanan = get_object_or_404(Perjalanan, pk=pk)
    
    # Inisialisasi data awal (ID perjalanan disembunyikan di form)
    initial_data = {'perjalanan': perjalanan.pk}

    if request.method == 'POST':
        # Mengisi form dengan data POST
        form = PemesananForm(request.POST)
        if form.is_valid():
            
            # Mendapatkan ID perjalanan dari field tersembunyi
            perjalanan_id = form.cleaned_data['perjalanan'] 
            
            # Simpan pemesanan tanpa commit (agar kita bisa menambahkan objek Perjalanan)
            booking = form.save(commit=False)
            booking.perjalanan = perjalanan # Menetapkan objek Perjalanan
            booking.save() # Menyimpan ke database, memicu perhitungan total_harga
            
            messages.success(request, f"Pemesanan ke {perjalanan.tujuan} berhasil! Total Harga: Rp {booking.total_harga:,.0f}")
            return redirect('trip_detail', pk=perjalanan.pk) # Redirect ke halaman detail
        else:
            messages.error(request, "Terdapat kesalahan input pada formulir. Mohon periksa kembali.")
    else:
        # Menampilkan form kosong dengan nilai awal ID perjalanan
        form = PemesananForm(initial=initial_data)

    context = {
        'perjalanan': perjalanan,
        'form': form
    }
    return render(request, 'travel/booking_form.html', context)