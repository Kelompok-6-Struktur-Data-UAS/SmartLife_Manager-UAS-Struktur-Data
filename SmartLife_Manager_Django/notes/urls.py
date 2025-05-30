from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.note_list_view, name='note_list'),
    path('buat/', views.note_create_view, name='note_create'),
    path('<int:note_id>/', views.note_detail_view, name='note_detail'), # Menggunakan int karena ID model
    path('<int:note_id>/edit/', views.note_update_view, name='note_update'),
    path('<int:note_id>/hapus/', views.note_delete_view, name='note_delete'),
]