# SmartLife_Manager_Django/notes/urls.py
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list_view, name='note_list'),
    path('buat/', views.note_create_view, name='note_create'),
    path('<str:note_id>/', views.note_detail_view, name='note_detail'), # Menggunakan str karena UUID
    path('<str:note_id>/edit/', views.note_update_view, name='note_update'),
    path('<str:note_id>/hapus/', views.note_delete_view, name='note_delete'),
]