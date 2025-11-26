from django.urls import path
from . import views

# PERBAIKI: Mengganti list_perjalanan dengan daftar_perjalanan
urlpatterns = [
    path('', views.daftar_perjalanan, name='list_perjalanan'), # <-- SUDAH DIKOREKSI
    # Jika ada path lain, tambahkan di sini...
<<<<<<< HEAD
    path('detail/<int:pk>/', views.trip_detail, name='trip_detail')
=======
>>>>>>> 3d801cc01599e8cb9137dcf56893ac12efc265d4
]