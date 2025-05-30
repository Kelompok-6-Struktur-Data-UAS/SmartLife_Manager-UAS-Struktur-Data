from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm # Form ubah password bawaan Django
from django.contrib.auth import update_session_auth_hash # Untuk menjaga sesi setelah ganti password
from .forms import UserProfileUpdateForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Untuk form update profil
        # Kita akan bedakan form update profil dan form ganti password berdasarkan nama tombol submit jika digabung
        # atau lebih baik buat view terpisah untuk ganti password
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('profiles:profile_view') # Kembali ke halaman profil
        else:
            messages.error(request, 'Gagal memperbarui profil. Silakan periksa error di bawah.')
    else:
        profile_form = UserProfileUpdateForm(instance=request.user)

    context = {
        'title': f'Profil Saya: {request.user.username}',
        'profile_form': profile_form,
        'struktur_data_info': "Informasi profil Anda disimpan dalam struktur data yang efisien di database (mirip Dictionary/Hash Table untuk akses cepat) dan terhubung dengan akun pengguna Anda."
    }
    return render(request, 'profiles/profile_page.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Penting agar user tidak logout!
            messages.success(request, 'Password Anda berhasil diubah!')
            return redirect('profiles:profile_view') # Kembali ke halaman profil
        else:
            messages.error(request, 'Gagal mengubah password. Silakan periksa error di bawah.')
    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        'title': 'Ubah Password',
        'password_form': password_form
    }
    return render(request, 'profiles/change_password_page.html', context)