# SmartLife_Manager_Django/schedule/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, date as date_obj  # Impor date sebagai date_obj


# Helper functions untuk mengelola jadwal di sesi
def get_schedule_from_session(session):
    schedule_list_str = session.get('schedule_events', [])
    events = []
    for item_str in schedule_list_str:
        try:  # Pastikan ada ':' di sini dan baris berikutnya diindentasi
            # Asumsi format penyimpanan: {'date_str': 'YYYY-MM-DD', 'time_str': 'HH:MM', 'title': '...', 'location': '...'}
            event_date = datetime.strptime(item_str['date_str'], '%Y-%m-%d').date()
            event_time = datetime.strptime(item_str['time_str'], '%H:%M').time()
            events.append({
                'date': event_date,
                'time': event_time,
                'title': item_str['title'],
                'location': item_str.get('location', '')
            })
        except (ValueError, KeyError) as e:  # Pastikan ada ':' di sini
            print(f"DEBUG: Error parsing schedule item from session: {item_str}, Error: {e}")
            continue  # Lewati item yang error

    # Urutkan berdasarkan tanggal, lalu waktu
    events.sort(key=lambda x: (x['date'], x['time']))
    return events


def save_schedule_to_session(session, schedule_events_with_objects):
    serializable_schedule = []
    for event in schedule_events_with_objects:
        serializable_schedule.append({
            'date_str': event['date'].strftime('%Y-%m-%d'),
            'time_str': event['time'].strftime('%H:%M'),
            'title': event['title'],
            'location': event.get('location', '')
        })
    session['schedule_events'] = serializable_schedule
    session.modified = True


def add_event_to_schedule_session(session, event_date_str, event_time_str, title, location=""):
    try:  # Pastikan ada ':' di sini dan baris berikutnya diindentasi
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        event_time = datetime.strptime(event_time_str, '%H:%M').time()
    except ValueError:  # Pastikan ada ':' di sini
        # Error ini akan ditangkap di view dan ditampilkan ke pengguna
        raise ValueError("Format tanggal (YYYY-MM-DD) atau waktu (HH:MM) salah.")

    current_schedule_objects = get_schedule_from_session(session)

    new_event = {
        'date': event_date,
        'time': event_time,
        'title': title,
        'location': location
    }
    current_schedule_objects.append(new_event)
    save_schedule_to_session(session, current_schedule_objects)  # Pengurutan terjadi di get_schedule_from_session


@login_required
def schedule_page_view(request):
    schedule_events = get_schedule_from_session(request.session)
    today = date_obj.today()

    todays_events = [event for event in schedule_events if event['date'] == today]

    now_time = datetime.now().time()  # Waktu saat ini untuk filter upcoming_events
    upcoming_events = [
        event for event in schedule_events
        if event['date'] > today or (event['date'] == today and event['time'] > now_time)
    ]
    # Filter untuk acara lampau (sebelum hari ini, atau hari ini tapi waktunya sudah lewat)
    past_events = [
        event for event in schedule_events
        if event['date'] < today or (event['date'] == today and event['time'] < now_time)
    ]
    # Pastikan past_events diurutkan dari yang paling baru ke paling lama jika diinginkan
    past_events.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    context = {
        'title': 'Jadwal Kegiatan Saya',
        'all_events': schedule_events,
        'todays_events': todays_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,  # Menambahkan past_events ke context
        'struktur_data_info': "Jadwal Anda ditampilkan sebagai Daftar Terurut (Sorted List) berdasarkan tanggal dan waktu. Untuk pencarian atau pemfilteran rentang tanggal yang lebih kompleks pada data besar, struktur data seperti Pohon Pencarian Biner (Binary Search Tree) bisa lebih efisien.",
        'today_date_display': today.strftime("%A, %d %B %Y")
    }
    return render(request, 'schedule/schedule_page.html', context)


@login_required
def add_event_view(request):
    if request.method == 'POST':
        title = request.POST.get('event_title')
        date_str = request.POST.get('event_date')
        time_str = request.POST.get('event_time')  # Sebelumnya ada typo 'Gist' di sini
        location = request.POST.get('event_location', '')

        if title and date_str and time_str:
            try:
                title = title.strip()
                date_str = date_str.strip()
                time_str = time_str.strip()
                location = location.strip()

                if not title:
                    messages.error(request, "Judul acara tidak boleh kosong.")
                else:
                    add_event_to_schedule_session(request.session, date_str, time_str, title, location)
                    messages.success(request, f"Acara '{title}' berhasil ditambahkan ke jadwal.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Judul, tanggal, dan waktu acara wajib diisi.")
        return redirect('schedule:schedule_list')

    return redirect('schedule:schedule_list')
