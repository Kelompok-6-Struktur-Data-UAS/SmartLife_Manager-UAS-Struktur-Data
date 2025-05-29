# SmartLife_Manager_Django/notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Jika Anda memisahkan logika, import dari note_logic.py
from .note_logic import (
    get_notes_from_session, add_note_to_session, 
    get_note_by_id_from_session, update_note_in_session, 
    delete_note_from_session
)
# Jika ingin menggunakan Django Forms nanti:
# from .forms import NoteForm 

@login_required
def note_list_view(request):
    notes = get_notes_from_session(request.session)
    # Urutkan catatan dari yang terbaru (berdasarkan asumsi append) atau berdasarkan field tanggal jika ada
    # Untuk contoh ini, kita bisa reverse list agar yang terakhir ditambahkan muncul paling atas
    context = {
        'title': 'Catatan Saya',
        'notes': reversed(notes), # Tampilkan yang terbaru dulu
        'struktur_data_info': "Catatan Anda disimpan dalam sebuah Daftar (List). Saat Anda melihat catatan, yang terakhir diakses bisa dikelola menggunakan Tumpukan (Stack) untuk fitur 'Terakhir Dilihat'."
    }
    return render(request, 'notes/note_list_page.html', context)

@login_required
def note_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('note_title')
        content = request.POST.get('note_content')

        if title and content:
            title = title.strip()
            content = content.strip()
            if title:
                add_note_to_session(request.session, title, content)
                messages.success(request, f"Catatan '{title}' berhasil dibuat.")
                return redirect('notes:note_list')
            else:
                messages.error(request, "Judul catatan tidak boleh kosong.")
        else:
            messages.error(request, "Judul dan isi catatan wajib diisi.")
        # Jika error, kembali ke form tambah dengan data yang sudah diisi (jika pakai Django Form)
        # Untuk sekarang, kita hanya redirect, data form hilang jika error
        return render(request, 'notes/note_form_page.html', {'title': 'Buat Catatan Baru', 'note_title': title, 'note_content': content})


    context = {'title': 'Buat Catatan Baru'}
    return render(request, 'notes/note_form_page.html', context)


@login_required
def note_detail_view(request, note_id):
    note = get_note_by_id_from_session(request.session, note_id)
    if not note:
        messages.error(request, "Catatan tidak ditemukan.")
        return redirect('notes:note_list')

    # Konsep Stack: Jika ingin implementasi "Last Viewed", Anda bisa push ID catatan ini ke stack di session.
    # last_viewed_stack = request.session.get('last_viewed_notes_stack', [])
    # if note_id in last_viewed_stack: last_viewed_stack.remove(note_id) # Hapus jika sudah ada, untuk dipindah ke atas
    # last_viewed_stack.append(note_id)
    # if len(last_viewed_stack) > 5: last_viewed_stack.pop(0) # Batasi ukuran stack
    # request.session['last_viewed_notes_stack'] = last_viewed_stack
    # request.session.modified = True

    context = {
        'title': f"Detail Catatan: {note.get('title', 'Tanpa Judul')}",
        'note': note
    }
    return render(request, 'notes/note_detail_page.html', context)

@login_required
def note_update_view(request, note_id):
    note = get_note_by_id_from_session(request.session, note_id)
    if not note:
        messages.error(request, "Catatan tidak ditemukan untuk diedit.")
        return redirect('notes:note_list')

    if request.method == 'POST':
        new_title = request.POST.get('note_title')
        new_content = request.POST.get('note_content')
        if new_title and new_content:
            new_title = new_title.strip()
            new_content = new_content.strip()
            if new_title:
                if update_note_in_session(request.session, note_id, new_title, new_content):
                    messages.success(request, f"Catatan '{new_title}' berhasil diperbarui.")
                    return redirect('notes:note_detail', note_id=note_id)
                else: # Seharusnya tidak terjadi jika note ditemukan di awal
                    messages.error(request, "Gagal memperbarui catatan.")
            else:
                messages.error(request, "Judul catatan tidak boleh kosong.")
        else:
            messages.error(request, "Judul dan isi catatan wajib diisi.")
        # Kembali ke form edit dengan data saat ini jika ada error
        # Untuk ini, lebih baik pakai Django Form yang bisa di-repopulate
        return render(request, 'notes/note_form_page.html', {
            'title': f"Edit Catatan: {note.get('title')}", 
            'note_id': note_id, # Untuk action form
            'note_title': new_title or note.get('title'), 
            'note_content': new_content or note.get('content')
        })

    context = {
        'title': f"Edit Catatan: {note.get('title')}",
        'note_id': note_id, # Untuk action form
        'note_title': note.get('title'),
        'note_content': note.get('content')
    }
    return render(request, 'notes/note_form_page.html', context)


@login_required
def note_delete_view(request, note_id):
    if request.method == 'POST': # Hanya proses delete jika POST (dari form konfirmasi)
        note = get_note_by_id_from_session(request.session, note_id)
        if note:
            note_title = note.get('title', 'Tanpa Judul')
            if delete_note_from_session(request.session, note_id):
                messages.success(request, f"Catatan '{note_title}' berhasil dihapus.")
            else: # Seharusnya tidak terjadi
                messages.error(request, "Gagal menghapus catatan.")
        else:
            messages.error(request, "Catatan tidak ditemukan untuk dihapus.")
        return redirect('notes:note_list')

    # Jika GET, bisa tampilkan halaman konfirmasi atau redirect (untuk contoh ini redirect)
    # Idealnya ada template konfirmasi
    note = get_note_by_id_from_session(request.session, note_id)
    if not note:
        messages.error(request, "Catatan tidak ditemukan.")
        return redirect('notes:note_list')
    # Untuk konfirmasi, Anda akan render template di sini
    # return render(request, 'notes/note_confirm_delete.html', {'note': note, 'title': 'Konfirmasi Hapus'})
    messages.warning(request, "Aksi ini memerlukan konfirmasi melalui tombol hapus di detail catatan.")
    return redirect('notes:note_detail', note_id=note_id)