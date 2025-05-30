from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list_view, name='goal_list'),
    path('buat/', views.goal_create_view, name='goal_create'), # Halaman khusus tambah tujuan
    path('<int:goal_id>/', views.goal_detail_view, name='goal_detail'),
    path('<int:goal_id>/edit/', views.goal_update_view, name='goal_update'),
    path('<int:goal_id>/hapus/', views.goal_delete_view, name='goal_delete'),
    # URL untuk sub-tugas (pembuatan sub-tugas dihandle di goal_detail_view)
    path('subtask/<int:subtask_id>/edit/', views.subtask_update_view, name='subtask_update'),
    path('subtask/<int:subtask_id>/hapus/', views.subtask_delete_view, name='subtask_delete'),
]