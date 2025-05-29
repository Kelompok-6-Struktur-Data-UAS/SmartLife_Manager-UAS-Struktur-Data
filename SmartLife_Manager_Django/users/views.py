# SmartLife_Manager_Django/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from datetime import datetime, timezone, time # Pastikan 'time' juga diimpor

# from django.contrib.auth.models import User # Tidak perlu jika tidak ada query User langsung

def register_view(request):
    print(
        f"DEBUG (register_view): Request method: {request.method}, User authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        if request.user.is_staff:
            print("DEBUG (register_view): User is staff, redirecting to admin_choice")
            return redirect('admin_choice')
        else:
            print("DEBUG (register_view): User is authenticated, redirecting to users:dashboard")
            return redirect('users:dashboard')

    if request.method == 'POST':
        print("DEBUG (register_view): Processing POST data")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("DEBUG (register_view): Form is valid")
            user = form.save()
            # login(request, user) # Dihapus agar redirect ke login page
            messages.success(request, f'Akun {user.username} berhasil dibuat! Silakan login.')
            print(f"DEBUG (register_view): User {user.username} created, redirecting to users:login")
            return redirect('users:login')
        else:
            print(f"DEBUG (register_view): Form is NOT valid. Errors: {form.errors.as_json()}")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label_tag(field.label)}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        print("DEBUG (register_view): Processing GET request")
        form = CustomUserCreationForm()

    print("DEBUG (register_view): Rendering register_page.html")
    return render(request, 'users/register_page.html', {'form': form, 'title': 'Register'})


def login_view(request):
    print(
        f"DEBUG (login_view): Request method: {request.method}, User authenticated SEBELUM PROSES: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"DEBUG (login_view): User SUDAH authenticated ({request.user.username}), redirecting...")
        if request.user.is_staff:
            print("DEBUG (login_view): User is staff, redirecting to admin_choice")
            return redirect('admin_choice')
        else:
            print("DEBUG (login_view): User is normal user, redirecting to users:dashboard")
            return redirect('users:dashboard')

    if request.method == 'POST':
        print("DEBUG (login_view): Processing POST data")
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("DEBUG (login_view): Form login IS VALID")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"DEBUG (login_view): Mencoba autentikasi untuk user: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Setelah login(), request.user.is_authenticated seharusnya True untuk request berikutnya
                print(
                    f"DEBUG (login_view): Autentikasi BERHASIL untuk user: {user.username}. Is staff: {user.is_staff}. User authenticated SETELAH login(): {request.user.is_authenticated}")
                messages.info(request, f'Selamat datang kembali, {username}!')
                if user.is_staff:
                    print("DEBUG (login_view): Redirecting to admin_choice")
                    return redirect('admin_choice')
                else:
                    print("DEBUG (login_view): Redirecting to users:dashboard")
                    return redirect('users:dashboard')
            else:
                print("DEBUG (login_view): Autentikasi GAGAL (user is None)")
                messages.error(request, 'Username atau password salah.')
        else:
            print(f"DEBUG (login_view): Form login TIDAK VALID. Errors: {form.errors.as_json()}")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label_tag(field.label)}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        print("DEBUG (login_view): Processing GET request")
        form = CustomAuthenticationForm()

    print("DEBUG (login_view): Merender login_page.html")
    return render(request, 'users/login_page.html', {'form': form, 'title': 'Login'})


@login_required
def logout_view(request):
    print(f"DEBUG (logout_view): User {request.user.username} melakukan logout.")
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    print("DEBUG (logout_view): Redirecting to home")
    return redirect('home') # Pastikan URL 'home' ada di urls.py utama


@login_required
def user_dashboard_view(request):
    print(
        f"DEBUG (user_dashboard_view): Diakses oleh {request.user.username}. User authenticated: {request.user.is_authenticated}")

    # CONTOH DATA DINAMIS (ganti dengan logika pengambilan data Anda sebenarnya dari model)
    # Pastikan semua nilai tanggal/waktu adalah objek datetime Python

    # 1. Data Tugas Prioritas
    priority_tasks_data = [
        {'name': 'Presentasi Proyek Akhir', 'due_date': datetime(2025, 6, 1, tzinfo=timezone.utc),
         'priority_level': 'high',
         'data_structure_used': 'Heap'},
        {'name': 'Refactor Kode Modul X', 'due_date': datetime(2025, 6, 3, tzinfo=timezone.utc),
         'priority_level': 'high',
         'data_structure_used': 'Priority Queue'},
        {'name': 'Beli Kebutuhan Mingguan', 'due_date': datetime(2025, 6, 5, tzinfo=timezone.utc),
         'priority_level': 'medium',
         'data_structure_used': 'List'},
    ]

    # 2. Data Jadwal Hari Ini
    try:
        today_schedule_data = [
            # Menggunakan objek datetime.time untuk 'time' jika hanya waktu
            {'time': time(9, 0), 'title': 'Daily Standup Meeting', 'location': 'Online',
             'data_structure_used': 'Sorted List'},
            {'time': time(14, 30), 'title': 'Diskusi Klien Y',
             'location': 'Ruang Rapat B', 'data_structure_used': 'BST'},
        ]
    except ValueError as e:
        print(f"DEBUG: Error parsing time for today_schedule_data: {e}")
        today_schedule_data = []

    # 3. Data Catatan Terbaru
    recent_notes_data = [
        {'title': 'Ide untuk Fitur Social Graph', 'updated_at': datetime(2025, 5, 28, 10, 0, 0, tzinfo=timezone.utc),
         'snippet': 'Gunakan pustaka Vis.js untuk visualisasi...', 'data_structure_used': 'Stack'},
        {'title': 'Daftar Bacaan Struktur Data', 'updated_at': datetime(2025, 5, 27, 15, 30, 0, tzinfo=timezone.utc),
         'snippet': 'Buku Cormen, Sedgewick...', 'data_structure_used': 'List'},
    ]

    # 4. Data Pengingat Sosial (Contoh)
    social_reminders_data = [
        {'event_name': 'Ulang Tahun Budi', 'contact_name': 'Budi', 'detail': 'Hari ini! Kirim ucapan.',
         'data_structure_used': 'Graph/Dict'},
        {'event_name': 'Follow-up', 'contact_name': 'Siti', 'detail': 'Tanyakan perkembangan proposal.',
         'data_structure_used': 'Hash Table'},
    ]

    # 5. Data Progress Tujuan (Contoh)
    goals_progress_data = [
        {'name': 'Menguasai Algoritma Graf', 'progress': 65, 'data_structure_used': 'Tree Hierarchy'},
        {'name': 'Menyelesaikan Dashboard Aplikasi', 'progress': 80, 'data_structure_used': 'Modular Design'},
    ]

    # 6. Data Info Struktur Data Aktif (Contoh)
    active_data_structures_info = [
        {'name': 'Heap', 'usage_description': f"{len(priority_tasks_data)} tugas prioritas ditampilkan.",
         'icon_class': 'fas fa-fire'},
        {'name': 'Antrean (Queue)', 'usage_description': "5 tugas baru menunggu di inbox.",
         'icon_class': 'fas fa-stream'},
        {'name': 'Pohon (Tree)', 'usage_description': f"{len(today_schedule_data)} jadwal terorganisir.",
         'icon_class': 'fas fa-calendar-alt'},
        {'name': 'Graf (Graph)', 'usage_description': "Jaringan relasi Anda divisualisasikan.",
         'icon_class': 'fas fa-project-diagram'},
        {'name': 'Tumpukan (Stack)', 'usage_description': f"{len(recent_notes_data)} catatan dengan riwayat akses.",
         'icon_class': 'fas fa-layer-group'},
        {'name': 'Hash Table', 'usage_description': "Pencarian data cepat.", 'icon_class': 'fas fa-search'},
    ]

    # 7. Data Tim Pembuat (Untuk Footer)
    team_members_data = ["Rizma", "Nama Teman 1", "Nama Teman 2", "Nama Teman 3", "Nama Teman 4",
                         "Nama Teman 5"]  # Ganti dengan nama tim Anda

    context = {
        'title': 'Dashboard Utama',
        # 'nama_pengguna': request.user.username, # 'user' objek sudah tersedia di template secara default
        'priority_tasks': priority_tasks_data,
        'today_schedule': today_schedule_data,
        'recent_notes': recent_notes_data,
        'social_reminders': social_reminders_data,
        'goals_progress': goals_progress_data,
        'active_data_structures': active_data_structures_info,
        'team_members': team_members_data,
    }
    # Pastikan nama template ini sesuai dengan lokasi file HTML Anda
    return render(request, 'users/dashboard.html', context)


@login_required
def admin_choice_view(request):
    print(f"DEBUG (admin_choice_view): Diakses oleh {request.user.username}. User is_staff: {request.user.is_staff}")
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
        print("DEBUG (admin_choice_view): User is not staff, redirecting to users:dashboard")
        return redirect('users:dashboard')
    context = {
        'title': 'Pilihan Admin',
        # 'nama_pengguna': request.user.username # 'user' objek sudah tersedia
    }
    print("DEBUG (admin_choice_view): Merender admin_choice.html")
    return render(request, 'admin_choice.html', context)