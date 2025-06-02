from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Halaman utama untuk fitur jadwal (menampilkan daftar/kalender dan bisa ada form tambah cepat)
    path('', views.schedule_list_view, name='schedule_list'),

    # URL untuk halaman khusus membuat acara baru
    path('acara/buat/', views.event_create_view, name='event_create'),

    # URL untuk melihat detail, mengedit, dan menghapus acara spesifik
    # (Tidak ada path untuk 'edit/' atau 'hapus/' secara umum, tapi spesifik per event_id)
    path('acara/<int:event_id>/edit/', views.event_update_view, name='event_update'),
    path('acara/<int:event_id>/hapus/', views.event_delete_view, name='event_delete'),

    # URL untuk tampilan FullCalendar (jika Anda menggunakannya)
    # Fungsi view 'schedule_page_view' harus ada di schedule/views.py jika path ini diaktifkan
    # Jika 'schedule_list_view' Anda sudah menampilkan kalender, Anda mungkin tidak perlu path ini.
    # Untuk sekarang, saya akan mengomentarinya agar tidak error jika view-nya belum ada.
    # path('kalender/', views.schedule_page_view, name='schedule_calendar'),

    # URL endpoint untuk FullCalendar mengambil data acara (jika Anda menggunakan FullCalendar)
    # Fungsi view 'all_events_json' harus ada di schedule/views.py jika path ini diaktifkan.
    # path('api/all_events/', views.all_events_json, name='all_events_json'),

    # CATATAN: Saya mengganti 'tambah/' menjadi 'acara/buat/' agar lebih konsisten dengan 'acara/edit/' dll.
    # dan menghapus path duplikat yang menggunakan 'add_event_view'.
    # Jika 'add_event_view' memiliki logika berbeda dari 'event_create_view', Anda bisa
    # memberinya nama path dan nama URL yang unik.
]