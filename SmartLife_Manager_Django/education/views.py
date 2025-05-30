# SmartLife_Manager_Django/education/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required # Jika hanya user login yang bisa lihat

# @login_required # Aktifkan jika halaman ini hanya untuk user yang sudah login
def about_app_view(request):
    context = {
        'title': 'Tentang SmartLife Manager',
        # Anda bisa menambahkan versi aplikasi atau informasi lain di sini jika perlu
    }
    return render(request, 'education/about_app_page.html', context)