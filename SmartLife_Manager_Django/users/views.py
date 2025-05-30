# SmartLife_Manager_Django/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from datetime import datetime, timezone, time, date as date_obj  # Pastikan date diimpor sebagai date_obj


# Komentar untuk User model bisa dihapus jika sudah jelas
# from django.contrib.auth.models import User

def register_view(request):
    print(f"DEBUG (register_view): Method: {request.method}, User Auth: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        if request.user.is_staff:
            print("DEBUG (register_view): Authenticated staff, redirecting to admin_choice")
            return redirect('admin_choice')
        else:
            print("DEBUG (register_view): Authenticated user, redirecting to users:dashboard")
            return redirect('users:dashboard')

    if request.method == 'POST':
        print("DEBUG (register_view): Processing POST data")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("DEBUG (register_view): Form is valid")
            user = form.save()
            messages.success(request, f'Akun {user.username} berhasil dibuat! Silakan login.')
            print(f"DEBUG (register_view): User {user.username} created, redirecting to users:login")
            return redirect('users:login')
        else:
            print(f"DEBUG (register_view): Form is NOT valid. Errors: {form.errors.as_json()}")
            # Menampilkan error ke pengguna melalui messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    # Menggunakan field.label jika ada, atau nama field jika tidak ada label eksplisit
                    field_label = form.fields[field].label if form.fields[field].label else field.replace('_',
                                                                                                          ' ').capitalize()
                    if field == '__all__':  # Error non-field
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field_label}: {error}")
    else:  # GET request
        print("DEBUG (register_view): Processing GET request")
        form = CustomUserCreationForm()

    print("DEBUG (register_view): Rendering register_page.html")
    return render(request, 'users/register_page.html', {'form': form, 'title': 'Register'})


def login_view(request):
    print(f"DEBUG (login_view): Method: {request.method}, User Auth (Before): {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"DEBUG (login_view): User '{request.user.username}' already authenticated, redirecting...")
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
            print(f"DEBUG (login_view): Authenticating user: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(
                    f"DEBUG (login_view): Auth SUCCESS for '{user.username}'. Staff: {user.is_staff}. Auth after login: {request.user.is_authenticated}")
                messages.info(request, f'Selamat datang kembali, {username}!')
                if user.is_staff:
                    print("DEBUG (login_view): Redirecting to admin_choice")
                    return redirect('admin_choice')
                else:
                    print("DEBUG (login_view): Redirecting to users:dashboard")
                    return redirect('users:dashboard')
            else:
                print("DEBUG (login_view): Auth FAILED (user is None or inactive)")
                messages.error(request, 'Username atau password salah, atau akun Anda tidak aktif.')
        else:
            print(f"DEBUG (login_view): Form login NOT VALID. Errors: {form.errors.as_json()}")
            for field, errors in form.errors.items():
                for error in errors:
                    field_label = form.fields[field].label if form.fields[field].label else field.replace('_',
                                                                                                          ' ').capitalize()
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field_label}: {error}")
    else:  # GET request
        print("DEBUG (login_view): Processing GET request")
        form = CustomAuthenticationForm()

    print("DEBUG (login_view): Rendering login_page.html")
    return render(request, 'users/login_page.html', {'form': form, 'title': 'Login'})


@login_required
def logout_view(request):
    print(f"DEBUG (logout_view): User {request.user.username} logging out.")
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    print("DEBUG (logout_view): Redirecting to home")
    return redirect('home')  # Pastikan URL 'home' ada


@login_required
def user_dashboard_view(request):
    print(f"DEBUG (user_dashboard_view): Accessed by {request.user.username}. Auth: {request.user.is_authenticated}")

    # CONTOH DATA DINAMIS (nantinya akan diambil dari model/database)
    # Data ini akan digunakan oleh template dashboard.html Anda
    # Pastikan key di sini sesuai dengan yang Anda gunakan di template.

    # 1. Data Tugas Prioritas (Contoh, nantinya dari model Task atau logika sesi Tasks)
    priority_tasks_data = [
        {'name': 'Presentasi Proyek Akhir', 'due_date': datetime(2025, 6, 1, tzinfo=timezone.utc),
         'priority_level': 'high', 'data_structure_used': 'Heap'},
        {'name': 'Refactor Kode Modul X', 'due_date': datetime(2025, 6, 3, tzinfo=timezone.utc),
         'priority_level': 'high', 'data_structure_used': 'Priority Queue'},
    ]

    # 2. Data Jadwal Hari Ini (Contoh, nantinya dari model Event di Schedule)
    try:
        today_schedule_data = [
            {'time': time(9, 0), 'title': 'Daily Standup', 'location': 'Online', 'data_structure_used': 'Sorted List'},
            {'time': time(14, 30), 'title': 'Diskusi Klien', 'location': 'Ruang Rapat B', 'data_structure_used': 'BST'},
        ]
    except ValueError as e:
        print(f"DEBUG: Error parsing time for today_schedule_data: {e}")
        today_schedule_data = []

    # 3. Data Catatan Terbaru (Contoh, nantinya dari model Note)
    recent_notes_data = [
        # Pastikan 'id' ada jika template Anda membutuhkannya untuk {% url 'notes:note_detail' note.id %}
        {'id': 1, 'title': 'Ide Fitur Social Graph', 'updated_at': datetime(2025, 5, 28, 10, 0, 0, tzinfo=timezone.utc),
         'snippet': 'Visualisasi jaringan pertemanan...', 'data_structure_used': 'Stack'},
        {'id': 2, 'title': 'Daftar Bacaan Struktur Data',
         'updated_at': datetime(2025, 5, 27, 15, 30, 0, tzinfo=timezone.utc), 'snippet': 'Buku referensi algoritma...',
         'data_structure_used': 'List'},
    ]

    # 4. Data Pengingat Sosial (Contoh, nantinya dari model Contact)
    social_reminders_data = [
        {'event_name': 'Ulang Tahun Budi', 'contact_name': 'Budi', 'detail': 'Hari ini! Kirim ucapan.',
         'data_structure_used': 'Graph/Dict'},
    ]

    # 5. Data Progress Tujuan (Contoh, nantinya dari model Goal)
    goals_progress_data = [
        {'name': 'Menguasai Algoritma Graf', 'progress': 65, 'data_structure_used': 'Tree Hierarchy'},
    ]

    # 6. Data Info Struktur Data Aktif (Statis atau bisa dinamis)
    active_data_structures_info = [
        {'name': 'Heap', 'usage_description': f"{len(priority_tasks_data)} tugas prioritas.",
         'icon_class': 'fas fa-fire'},
        {'name': 'Antrean (Queue)', 'usage_description': "Tugas masuk diproses FIFO.", 'icon_class': 'fas fa-stream'},
        # Tambahkan info struktur data lain yang relevan
    ]

    # 7. Data Tim Pembuat (Untuk Footer)
    team_members_data = ["Rizma", "Tim Member 2", "Tim Member 3", "Tim Member 4", "Tim Member 5", "Tim Member 6"]

    context = {
        'title': 'Dashboard Utama',
        # 'nama_pengguna': request.user.username, # 'user' objek sudah otomatis tersedia di template
        'priority_tasks': priority_tasks_data,
        'today_schedule': today_schedule_data,
        'recent_notes': recent_notes_data,
        'social_reminders': social_reminders_data,
        'goals_progress': goals_progress_data,
        'active_data_structures': active_data_structures_info,
        'team_members': team_members_data,
        'today_date_display': date_obj.today().strftime("%A, %d %B %Y")  # Tambahkan jika belum ada
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def admin_choice_view(request):
    print(f"DEBUG (admin_choice_view): Accessed by {request.user.username}. Staff: {request.user.is_staff}")
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
        print("DEBUG (admin_choice_view): Not staff, redirecting to users:dashboard")
        return redirect('users:dashboard')
    context = {
        'title': 'Pilihan Admin',
    }
    print("DEBUG (admin_choice_view): Rendering admin_choice.html")
    return render(request, 'admin_choice.html', context)