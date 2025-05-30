# SmartLife_Manager_Django/tasks/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import deque  # Untuk implementasi Queue


# Helper function untuk mendapatkan queue dari session
def get_task_queue_from_session(session):
    # Mengambil queue dari sesi, atau membuat list kosong baru jika tidak ada.
    # Kita simpan sebagai list di session karena deque tidak JSON serializable secara default.
    task_list = session.get('task_queue', [])  # Default ke list kosong jika key tidak ada
    return deque(task_list)  # Ubah kembali ke deque saat digunakan


def save_task_queue_to_session(session, task_deque):
    # Simpan deque sebagai list ke dalam session
    session['task_queue'] = list(task_deque)
    session.modified = True  # Tandai bahwa session telah dimodifikasi


@login_required
def task_queue_view(request):
    print(f"DEBUG (tasks/task_queue_view): Diakses oleh {request.user.username}")
    current_task_queue = get_task_queue_from_session(request.session)

    context = {
        'title': 'Antrean Tugas Saya (Queue)',
        'tasks': list(current_task_queue),  # Kirim sebagai list ke template untuk iterasi
        'next_task': current_task_queue[0] if current_task_queue else None,
        'struktur_data_info': "Tugas Anda dikelola dalam sebuah Antrean (Queue) menggunakan prinsip First-In, First-Out (FIFO). Tugas yang pertama masuk akan pertama keluar untuk diproses."
    }
    return render(request, 'tasks/task_queue_page.html', context)


@login_required
def add_task_view(request):
    print(f"DEBUG (tasks/add_task_view): Request method: {request.method}")
    if request.method == 'POST':
        task_description = request.POST.get('task_description')
        print(f"DEBUG (tasks/add_task_view): Deskripsi Tugas dari POST: '{task_description}'")

        if task_description and task_description.strip():  # Pastikan tidak kosong atau hanya spasi
            cleaned_task_description = task_description.strip()
            current_task_queue = get_task_queue_from_session(request.session)
            current_task_queue.append(cleaned_task_description)  # Tambah ke belakang antrean
            save_task_queue_to_session(request.session, current_task_queue)
            messages.success(request, f"Tugas '{cleaned_task_description}' telah ditambahkan ke antrean.")
            print(f"DEBUG (tasks/add_task_view): Tugas '{cleaned_task_description}' ditambahkan.")
        else:
            messages.error(request, "Deskripsi tugas tidak boleh kosong.")
            print("DEBUG (tasks/add_task_view): Deskripsi tugas kosong.")
    # Selalu redirect kembali ke halaman antrean setelah POST atau jika GET
    return redirect('tasks:task_queue')


@login_required
def process_task_view(request):
    print(f"DEBUG (tasks/process_task_view): Request method: {request.method}")
    if request.method == 'POST':  # Sebaiknya ini hanya diakses via POST
        current_task_queue = get_task_queue_from_session(request.session)
        if current_task_queue:
            processed_task = current_task_queue.popleft()  # Ambil & hapus dari depan antrean
            save_task_queue_to_session(request.session, current_task_queue)
            messages.info(request, f"Tugas '{processed_task}' telah diproses dan dihapus.")
            print(f"DEBUG (tasks/process_task_view): Tugas '{processed_task}' diproses.")
        else:
            messages.warning(request, "Tidak ada tugas untuk diproses.")
            print("DEBUG (tasks/process_task_view): Tidak ada tugas untuk diproses.")
    # Selalu redirect kembali ke halaman antrean setelah POST atau jika GET
    return redirect('tasks:task_queue')