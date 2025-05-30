# SmartLife_Manager_Django/smartlife_config/urls.py
from django.contrib import admin
from django.urls import path, include
# 'render' tidak lagi dibutuhkan di sini jika home_view tidak dipakai
from users.views import admin_choice_view, login_view  # Impor view yang dibutuhkan

urlpatterns = [
    path('admin_panel/', admin.site.urls),  # Panel Admin Django

    # URL Aplikasi Utama
    path('accounts/', include('users.urls')),  # Untuk login, register, dashboard user, logout
    path('manajemen-tugas/', include('tasks.urls')),
    path('jadwal-kegiatan/', include('schedule.urls')),
    path('catatan-saya/', include('notes.urls')),
    path('tujuan-prioritas/', include('goals.urls')),
    path('relasi-sosial/', include('contacts.urls')),
    path('edukasi/', include('education.urls')),
    path('profil-saya/', include('profiles.urls')),

    # URL Khusus
    path('admin-area/choice/', admin_choice_view, name='admin_choice'),  # URL untuk pilihan admin (hanya satu entri)

    # URL Root (Halaman Utama)
    # Path root sekarang mengarah ke halaman login.
    # Jika user sudah login, view login akan redirect ke dashboard/admin_choice.
    path('', login_view, name='home'),  # Hanya satu entri untuk path root
]