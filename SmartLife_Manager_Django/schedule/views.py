from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  # Untuk view yang hanya menerima POST
from .models import Event
from .forms import EventForm
from django.utils import timezone  # Untuk timezone.now() jika diperlukan
from datetime import date as date_obj, datetime, time  # Impor yang dibutuhkan


@login_required
def schedule_list_view(request):
    # Form untuk tambah cepat (akan diproses jika method POST)
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, f"Acara '{event.title}' berhasil ditambahkan melalui form cepat.")
            return redirect('schedule:schedule_list')  # Redirect untuk membersihkan POST
        else:
            # Jika form tidak valid, kita tetap perlu mengambil data event untuk ditampilkan
            # dan form yang tidak valid akan dikirim ke template untuk menampilkan error
            messages.error(request, "Gagal menambahkan acara melalui form cepat. Periksa input Anda.")
            # Biarkan form yang tidak valid dikirim ke context di bawah
    else:
        form = EventForm()  # Form kosong untuk GET request atau jika POST gagal dan ingin form baru

    # Mengambil semua acara milik pengguna yang sedang login
    all_user_events = Event.objects.filter(user=request.user).order_by('event_date', 'event_time')

    today = date_obj.today()
    now_datetime = timezone.now()  # Waktu saat ini yang timezone-aware

    todays_events = []
    upcoming_events = []
    past_events = []

    for event in all_user_events:
        event_datetime_naive = datetime.combine(event.event_date, event.event_time)
        # Jadikan event_datetime aware menggunakan default timezone jika naive
        if timezone.is_naive(event_datetime_naive):
            event_datetime_aware = timezone.make_aware(event_datetime_naive, timezone.get_default_timezone())
        else:
            event_datetime_aware = event_datetime_naive

        if event.event_date == today:
            todays_events.append(event)
        elif event_datetime_aware > now_datetime:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    # Mengurutkan past_events dari yang terbaru ke terlama (opsional, karena default model sudah mengurutkan)
    # Jika Anda ingin urutan berbeda dari default model untuk past_events:
    # past_events.sort(key=lambda x: (x.event_date, x.event_time), reverse=True)

    context = {
        'title': 'Jadwal Kegiatan Saya',
        'form': form,  # Untuk form tambah cepat di halaman list
        'todays_events': todays_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'struktur_data_info': "Jadwal Anda disimpan di database dan diurutkan. Indeks database (mirip BST) membantu pencarian cepat.",
        'today_date_display': today.strftime("%A, %d %B %Y")
    }
    return render(request, 'schedule/schedule_list_page.html', context)


@login_required
def event_create_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # Kaitkan acara dengan pengguna yang login
            event.save()
            messages.success(request, f"Acara '{event.title}' berhasil dibuat.")
            return redirect('schedule:schedule_list')  # Kembali ke daftar jadwal
        else:
            messages.error(request, "Gagal membuat acara. Periksa kembali isian form.")
            # Form dengan error akan dirender kembali oleh blok di bawah
    else:  # GET request
        form = EventForm()

    context = {
        'title': 'Tambah Acara Baru',
        'form': form
    }
    return render(request, 'schedule/event_form_page.html', context)


@login_required
def event_update_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)  # Keamanan: pastikan user hanya edit acaranya
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)  # Isi form dengan data acara yang ada
        if form.is_valid():
            form.save()
            messages.success(request, f"Acara '{event.title}' berhasil diperbarui.")
            return redirect(
                'schedule:schedule_list')  # Atau redirect ke detail: redirect('schedule:event_detail', event_id=event.id)
        else:
            messages.error(request, "Gagal memperbarui acara. Periksa kembali isian form.")
    else:  # GET request
        form = EventForm(instance=event)  # Tampilkan form dengan data acara saat ini

    context = {
        'title': f'Edit Acara: {event.title}',
        'form': form,
        'event': event  # Untuk digunakan di template jika perlu (misalnya, untuk link "Batal")
    }
    return render(request, 'schedule/event_form_page.html', context)


@login_required
@require_POST  # Hanya izinkan metode POST untuk aksi delete
def event_delete_view(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)  # Keamanan
    event_title = event.title
    event.delete()
    messages.success(request, f"Acara '{event_title}' berhasil dihapus.")
    return redirect('schedule:schedule_list')

# Jika Anda ingin halaman konfirmasi untuk GET request pada delete:
# @login_required
# def event_delete_confirm_view(request, event_id):
#     event = get_object_or_404(Event, id=event_id, user=request.user)
#     context = {
#         'title': f'Konfirmasi Hapus: {event.title}',
#         'event': event
#     }
#     return render(request, 'schedule/event_confirm_delete.html', context)
# Dan di urls.py, path untuk delete akan ke view ini, lalu form di confirm_delete akan POST ke event_delete_view