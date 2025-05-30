from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list_view, name='contact_list'),
    path('tambah/', views.contact_create_view, name='contact_create'),
    path('<int:contact_id>/', views.contact_detail_view, name='contact_detail'),
    path('<int:contact_id>/edit/', views.contact_update_view, name='contact_update'),
    path('<int:contact_id>/hapus/', views.contact_delete_view, name='contact_delete'),
]