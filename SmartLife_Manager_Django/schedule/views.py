# SmartLife_Manager_Django/schedule/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.utils import timezone
from datetime import date as date_obj  # Alias untuk menghindari konflik nama


@login_required
def schedule_list_view(request):
    # Mengambil semua acara milik pengguna yang sedang login, diurutkan berdasarkan tanggal dan waktu
    events = Event.objects.filter(user=request.user).order_by('event_date', 'event_time')

    today = date_obj.today()
    todays_events = events.filter(event_date=today)
    upcoming_events = events.filter(event_date__gt=today)  # Acara setelah hari ini
    past_events = events.filter(event_date__lt=today)  # Acara sebelum hari ini

    if request.method == 'POST':  # Ini untuk form tambah cepat di halaman list
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, f"Acara '{event.title}' berhasil ditambahkan.")
            return redirect('schedule:schedule_list')
        else:
            messages.error(request, "Gagal menambahkan acara. Silakan periksa input Anda.")
            # Kirim form yang tidak valid kembali ke template agar error bisa ditampilkan
    else:
        form = EventForm()  # Form kosong untuk GET request

    context = {
        'title': 'Jadwal Kegiatan Saya',
        'form': form,  # Untuk form tambah cepat
        'all_events': events,
        'todays_events': todays_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'struktur_data_info': "Jadwal Anda disimpan dan diurutkan berdasarkan tanggal & waktu. Database menggunakan indeks (mirip BST) untuk pencarian cepat.",
        'today_date_display': today.strftime("%A, %d %B %Y")
    }
    return render(request, 'schedule/schedule_list_page.html', context)


@login_required
def event_create_view(request):  # View terpisah jika ingin halaman khusus tambah acara
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, f"Acara '{event.title}' berhasil dibuat.")
            return redirect('schedule:schedule_list')
        else:
            messages.error(request, "Gagal membuat acara. Periksa kembali isian form.")
    else:
        form = EventForm()
    context = {
        'title': 'Tambah Acara Baru',
        'form': form
    }
    return render(request, 'schedule/event_form_page.html', context)  # Template form terpisah


@login_required
def event_update_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)  # Pastikan user hanya bisa edit acaranya sendiri
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Acara '{event.title}' berhasil diperbarui.")
            return redirect('schedule:schedule_list')
        else:
            messages.error(request, "Gagal memperbarui acara. Periksa kembali isian form.")
    else:
        form = EventForm(instance=event)
    context = {
        'title': f'Edit Acara: {event.title}',
        'form': form,
        'event': event  # Untuk menampilkan detail acara yang diedit jika perlu
    }
    return render(request, 'schedule/event_form_page.html', context)  # Bisa pakai template form yang sama


@login_required
def event_delete_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':  # Konfirmasi penghapusan biasanya dilakukan dengan POST
        event_title = event.title
        event.delete()
        messages.success(request, f"Acara '{event_title}' berhasil dihapus.")
        return redirect('schedule:schedule_list')

    # Jika GET, tampilkan halaman konfirmasi (atau langsung hapus jika tidak perlu konfirmasi)
    # Untuk contoh ini, kita langsung hapus jika POST, dan redirect jika GET
    # Idealnya ada halaman konfirmasi
    # return render(request, 'schedule/event_confirm_delete.html', {'event': event, 'title': 'Konfirmasi Hapus Acara'})
    messages.warning(request, "Aksi penghapusan memerlukan konfirmasi.")
    return redirect('schedule:schedule_list')