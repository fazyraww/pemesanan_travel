"""
ASGI config for pemesanan_travel project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Baris ini diubah: 'data_kelurahan.settings' diganti menjadi 'pemesanan_travel.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pemesanan_travel.settings')

application = get_asgi_application()