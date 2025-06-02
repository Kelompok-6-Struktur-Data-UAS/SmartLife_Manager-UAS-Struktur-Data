from django.shortcuts import render
# from django.contrib.auth.decorators import login_required # Aktifkan jika halaman ini hanya untuk user yang sudah login

# @login_required # Aktifkan jika perlu
def about_app_view(request):
    team_members_data = [
        {'name': 'RIZMA INDRA PRAMUDYA', 'role': 'NIM 24111814117', 'contribution': 'Project Lead / Full-Stack Developer'},
        {'name': 'Naufal Yudantara Saputra', 'role': 'NIM 24111814023', 'contribution': 'help lend a device' },
        {'name': 'Bagus Adibrata', 'role': 'NIM 24111814090', 'contribution': 'Front-end' },
        {'name': 'Dedi Firmansyah', 'role': 'NIM 24111814021','contribution': 'article editor' },
        {'name': 'Given Dimas Ara Dea', 'role': 'NIM 24111814101', },
        # Anda bisa menambahkan satu anggota lagi jika timnya 6 orang,
        # atau sesuaikan deskripsi peran/kontribusi di atas.
        # {'name': 'Nama Anggota Ke-6', 'role': 'NIM XXXXX', 'contribution': 'Peran Anggota Ke-6'},
    ]
    context = {
        'title': 'Tentang SmartLife Manager',
        'team_members_with_roles': team_members_data,
        'struktur_data_info': "Halaman ini menjelaskan visi, misi, dan fitur utama dari aplikasi SmartLife Manager." # Contoh deskripsi
    }
    return render(request, 'education/about_app_page.html', context)