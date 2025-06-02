from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from datetime import datetime, timezone, time, date as date_obj

# --- IMPORT MODEL DARI APLIKASI LAIN & HELPER UNTUK TASKS ---
# (Uncomment dan sesuaikan dengan nama model dan aplikasi Anda)
from tasks.views import get_task_queue_from_session # Untuk mengambil data tugas dari sesi
from schedule.models import Event  # Asumsi model Anda bernama Event di app schedule
from notes.models import Note      # Asumsi model Anda bernama Note di app notes
from goals.models import Goal      # Asumsi model Anda bernama Goal di app goals
from contacts.models import Contact  # Asumsi model Anda bernama Contact di app contacts
# --------------------------------------------------------------------

# ... (fungsi register_view, login_view, logout_view, admin_choice_view Anda tetap sama) ...
# Pastikan fungsi-fungsi tersebut ada di sini jika belum disalin dari contoh sebelumnya.

def register_view(request):
    # ... (kode register_view Anda yang sudah ada) ...
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
            for field, errors_list in form.errors.items(): # Menggunakan items() untuk iterasi yang benar
                for error in errors_list:
                    field_object = form.fields.get(field) # Dapatkan objek field untuk akses label
                    field_label = field_object.label if field_object and field_object.label else field.replace('_',' ').capitalize()
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field_label}: {error}")
    else: # GET request
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
                print(f"DEBUG (login_view): Auth SUCCESS for '{user.username}'. Staff: {user.is_staff}. Auth after login: {request.user.is_authenticated}")
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
            for field, errors_list in form.errors.items():
                for error in errors_list:
                    field_object = form.fields.get(field)
                    field_label = field_object.label if field_object and field_object.label else field.replace('_',' ').capitalize()
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        messages.error(request, f"{field_label}: {error}")
    else: # GET request
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
    return redirect('home')


@login_required
def user_dashboard_view(request):
    print(f"DEBUG (user_dashboard_view): Accessed by {request.user.username}. Auth: {request.user.is_authenticated}")
    current_user = request.user
    today = date_obj.today() # date_obj dari import datetime

    # 1. Data Tugas (dari sesi)
    task_queue_deque = get_task_queue_from_session(request.session)
    # Format untuk template dashboard (ambil beberapa contoh)
    priority_tasks_data = [
        {'name': task_desc, 'due_date': None, 'priority_level': 'medium', 'data_structure_used': 'Queue'}
        for task_desc in list(task_queue_deque)[:3] # Ambil 3 tugas pertama
    ]

    # 2. Data Jadwal Hari Ini (Dari model Event)
    try:
        today_schedule_queryset = Event.objects.filter(user=current_user, event_date=today).order_by('event_time')
        today_schedule_data = [
            {'time': event.event_time, 'title': event.title, 'location': event.location, 'data_structure_used': 'Sorted List/DB'}
            for event in today_schedule_queryset
        ]
    except Exception as e:
        print(f"Error mengambil data jadwal dari DB: {e}")
        today_schedule_data = []

    # 3. Data Catatan Terbaru (Dari model Note)
    try:
        recent_notes_queryset = Note.objects.filter(user=current_user).order_by('-updated_at')[:3] # Ambil 3 terbaru
        recent_notes_data = []
        for note_obj in recent_notes_queryset:
            recent_notes_data.append({
                'id': note_obj.id, # Penting untuk link detail
                'title': note_obj.title,
                'updated_at': note_obj.updated_at, # Ini sudah objek datetime
                'snippet': note_obj.content, # Anda akan memotongnya di template
                'data_structure_used': 'List/DB'
            })
    except Exception as e:
        print(f"Error mengambil data catatan dari DB: {e}")
        recent_notes_data = []

    # 4. Data Pengingat Sosial (Dari model Contact - Contoh Sederhana)
    try:
        # Contoh: ambil kontak yang ulang tahun bulan ini (logika bisa lebih kompleks)
        # contacts_birthday_this_month = Contact.objects.filter(user=current_user, birthday__month=today.month).order_by('birthday__day')[:2]
        # social_reminders_data = [
        #     {'event_name': f"Ulang Tahun {c.name}", 'contact_name': c.name, 'detail': c.birthday.strftime('%d %b'), 'data_structure_used': 'Graph/Dict'}
        #     for c in contacts_birthday_this_month
        # ]
        # Untuk sekarang, kita kosongkan dulu:
        social_reminders_data = []
    except Exception as e:
        print(f"Error mengambil data kontak dari DB: {e}")
        social_reminders_data = []

    # 5. Data Progress Tujuan (Dari model Goal - Contoh Sederhana)
    try:
        # goals_queryset = Goal.objects.filter(user=current_user, is_completed=False).order_by('-priority')[:2]
        # goals_progress_data = [
        #     {'name': goal.title, 'progress': goal.get_progress_percentage(), 'data_structure_used': 'Tree/DB'}
        #     for goal in goals_queryset
        # ]
        # Untuk sekarang, kita kosongkan dulu:
        goals_progress_data = []
    except Exception as e:
        print(f"Error mengambil data tujuan dari DB: {e}")
        goals_progress_data = []


    # 6. Data Info Struktur Data Aktif (Bisa lebih dinamis)
    active_data_structures_info = [
        {'name': 'Antrean (Queue)', 'usage_description': f"{len(task_queue_deque)} tugas di antrean.", 'icon_class': 'fas fa-stream'},
        {'name': 'Database (Sorted List/Index)', 'usage_description': f"{len(schedule_events) if 'schedule_events' in locals() else 0} jadwal & {len(recent_notes_data)} catatan.", 'icon_class': 'fas fa-database'},
        # Tambahkan info lain berdasarkan data yang berhasil diambil
    ]

    team_members_data = ["Rizma", "Tim Anda", "Anggota 3", "Anggota 4", "Anggota 5", "Anggota 6"]

    context = {
        'title': 'Dashboard Utama',
        'priority_tasks': priority_tasks_data,
        'today_schedule': today_schedule_data,
        'recent_notes': recent_notes_data,
        'social_reminders': social_reminders_data,
        'goals_progress': goals_progress_data,
        'active_data_structures': active_data_structures_info,
        'team_members': team_members_data,
        'today_date_display': today.strftime("%A, %d %B %Y")
    }
    return render(request, 'users/dashboard.html', context)


@login_required
def admin_choice_view(request):
    print(f"DEBUG (admin_choice_view): Accessed by {request.user.username}. Staff: {request.user.is_staff}")
    if not request.user.is_staff:
        messages.error(request, "Halaman ini hanya untuk admin. Silakan login dengan akun admin.")
        print("DEBUG (admin_choice_view): User is not staff, logging out and redirecting to login page")
        logout(request)  # Logout pengguna saat ini agar form login bersih
        return redirect('users:login')  # Arahkan ke halaman login

    # Jika pengguna adalah staf/admin, tampilkan halaman pilihan admin
    context = {
        'title': 'Pilihan Admin',
    }
    print("DEBUG (admin_choice_view): Rendering admin_choice.html")
    return render(request, 'admin_choice.html', context)