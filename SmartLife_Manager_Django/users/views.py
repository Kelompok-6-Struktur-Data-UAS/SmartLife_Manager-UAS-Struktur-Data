from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
# from django.contrib.auth.models import User # Hanya jika perlu query User secara langsung

def register_view(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrasi berhasil! Anda sekarang sudah login.')
            return redirect('users:dashboard')
        else:
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{form.fields[field].label if field != '__all__' else ''}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register_page.html', {'form': form, 'title': 'Register'})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_choice')
        else:
            return redirect('users:dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Selamat datang kembali, {username}!')
                if user.is_staff:
                    return redirect('admin_choice')
                else:
                    return redirect('users:dashboard')
            else:
                messages.error(request, 'Username atau password salah.')
        else:
             for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{form.fields[field].label if field != '__all__' else ''}: {error}")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login_page.html', {'form': form, 'title': 'Login'})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Anda telah berhasil logout.')
    return redirect('home')

@login_required
def user_dashboard_view(request):
    return render(request, 'users/dashboard.html', {'title': 'Dashboard Pengguna'})

@login_required
def admin_choice_view(request): # Pindahkan ini ke aplikasi admin nanti jika perlu
    if not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
        return redirect('users:dashboard')
    return render(request, 'admin_choice.html', {'title': 'Pilihan Admin'})