from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Perjalanan, Pemesanan, Ulasan  # Pastikan import model
from .forms import PemesananForm  # Pastikan import form

# Fungsi API (tidak diubah)
def daftar_perjalanan_api(request):
    perjalanan_list = Perjalanan.objects.all().values('id', 'nama', 'harga')
    return JsonResponse(list(perjalanan_list), safe=False)

# Fungsi daftar perjalanan (tidak diubah)
def daftar_perjalanan(request):
    semua_perjalanan = Perjalanan.objects.all().order_by('tgl_berangkat')
    context = {'perjalanan_list': semua_perjalanan}
    return render(request, 'travel/trip_list.html', context)

# Fungsi detail perjalanan (PERBAIKAN UTAMA: Tambah pemesanan_list)
def trip_detail(request, pk):
    """Menampilkan detail perjalanan dan daftar pemesanan terkait."""
    perjalanan = get_object_or_404(Perjalanan, pk=pk)
    
    # Ambil daftar pemesanan untuk perjalanan ini (menggunakan related_name 'pemesanan')
    pemesanan_list = perjalanan.pemesanan.all()  # Ini yang membuat data muncul
    
    context = {
        'perjalanan': perjalanan,
        'pemesanan_list': pemesanan_list  # Kirim ke template
    }
    return render(request, 'travel/trip_detail.html', context)

# Fungsi booking (tidak diubah)
def booking_create(request, pk):
    perjalanan = get_object_or_404(Perjalanan, pk=pk)
    initial_data = {'perjalanan': perjalanan.pk}
    
    if request.method == 'POST':
        form = PemesananForm(request.POST)
        if form.is_valid():
            perjalanan_id = form.cleaned_data['perjalanan']
            booking = form.save(commit=False)
            booking.perjalanan = perjalanan
            booking.save()
            messages.success(request, f"Pemesanan ke {perjalanan.tujuan} berhasil! Total Harga: Rp {booking.total_harga:,.0f}")
            return redirect('trip_detail', pk=perjalanan.pk)
        else:
            messages.error(request, "Terdapat kesalahan input pada formulir. Mohon periksa kembali.")
    else:
        form = PemesananForm(initial=initial_data)
    
    context = {'perjalanan': perjalanan, 'form': form}
    return render(request, 'travel/booking_form.html', context)