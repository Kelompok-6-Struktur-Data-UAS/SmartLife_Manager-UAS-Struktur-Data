# SmartLife_Manager_Django/smartlife_config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from users.views import admin_choice_view, login_view # Impor login_view dari users.views

# Hapus view home_view jika root akan diarahkan ke login
# def home_view(request):
#     return render(request, 'index.html', {'title': 'Home SmartLife Manager'})

urlpatterns = [
    path('admin_panel/', admin.site.urls), # Panel Admin Django
    path('accounts/', include('users.urls')), # URL untuk login, register, dashboard user dari aplikasi 'users'
    path('admin-area/choice/', admin_choice_view, name='admin_choice'), # URL untuk pilihan admin
    path('', login_view, name='home'), # Path root sekarang mengarah ke halaman login
                                        # Jika user sudah login, view login akan redirect
]