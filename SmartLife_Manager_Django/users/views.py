# SmartLife_Manager_Django/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm


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
    return redirect('home')


@login_required
def user_dashboard_view(request):
    print(
        f"DEBUG (user_dashboard_view): Diakses oleh {request.user.username}. User authenticated: {request.user.is_authenticated}")
    context = {
        'title': 'Dashboard Pengguna',
        'nama_pengguna': request.user.username
    }
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
        'nama_pengguna': request.user.username
    }
    print("DEBUG (admin_choice_view): Merender admin_choice.html")
    return render(request, 'admin_choice.html', context)