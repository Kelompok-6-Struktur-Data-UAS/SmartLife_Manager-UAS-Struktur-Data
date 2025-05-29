# SmartLife_Manager_Django/schedule/urls.py
from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('', views.schedule_list_view, name='schedule_list'),          # Daftar semua acara & form tambah cepat
    path('tambah/', views.event_create_view, name='event_create'),     # Halaman khusus tambah acara
    path('edit/<int:event_id>/', views.event_update_view, name='event_update'),
    path('hapus/<int:event_id>/', views.event_delete_view, name='event_delete'),
]