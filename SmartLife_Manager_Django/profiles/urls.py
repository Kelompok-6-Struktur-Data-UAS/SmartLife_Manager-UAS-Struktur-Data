from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.profile_view, name='profile_view'), # Halaman utama profil & update info dasar
    path('ubah-password/', views.change_password_view, name='change_password'),
]