from django import forms
from .models import Pemesanan

# Definisi formulir Pemesanan
class PemesananForm(forms.ModelForm):
    # Field 'perjalanan' dijadikan hidden input karena nilainya akan 
    # diisi otomatis dari URL (trip_detail)
    perjalanan = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = Pemesanan
        # Hanya menampilkan nama pelanggan dan jumlah orang
        fields = ['nama_pelanggan', 'jumlah_orang', 'perjalanan']
        widgets = {
            'nama_pelanggan': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Masukkan nama lengkap Anda',
            }),
            'jumlah_orang': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500',
                'min': 1, # Minimal 1 orang
            }),
        }

    # Custom clean untuk memastikan jumlah orang minimal 1
    def clean_jumlah_orang(self):
        jumlah = self.cleaned_data.get('jumlah_orang')
        if jumlah is None or jumlah < 1:
            raise forms.ValidationError("Jumlah orang harus minimal 1.")
        return jumlah