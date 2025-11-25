from django import forms
from .models import Pemesanan

class PemesananForm(forms.ModelForm):
    # Field 'perjalanan' akan disembunyikan karena nilainya disetel di view
    perjalanan = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model = Pemesanan
        fields = ['perjalanan', 'nama_pelanggan', 'jumlah_orang']
        widgets = {
            'nama_pelanggan': forms.TextInput(attrs={'placeholder': 'Masukkan nama lengkap Anda'}),
            'jumlah_orang': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }