from django.apps import AppConfig

class TravelConfig(AppConfig):
    # Mengganti default auto field, sudah diatur di settings.py
    default_auto_field = 'django.db.models.BigAutoField'
    # Nama aplikasi (penting untuk diinstal di settings.py)
    name = 'travel'
    # Nama yang lebih mudah dibaca untuk tampilan di Admin (opsional)
    verbose_name = 'Pemesanan dan Paket Travel'