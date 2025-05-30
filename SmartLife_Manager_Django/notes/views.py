# SmartLife_Manager_Django/notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST  # <-- TAMBAHKAN IMPORT INI
from .models import Note
from .forms import NoteForm


@login_required
def note_list_view(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    context = {
        'title': 'Semua Catatan Saya',
        'notes': notes,
        'struktur_data_info': "Catatan Anda ditampilkan sebagai Daftar (List) yang diurutkan berdasarkan waktu terakhir diubah. Konsep Tumpukan (Stack) bisa digunakan untuk fitur 'Catatan Terakhir Dilihat'."
    }
    return render(request, 'notes/note_list_page.html', context)


@login_required
def note_detail_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    context = {
        'title': note.title,
        'note': note
    }
    return render(request, 'notes/note_detail_page.html', context)


@login_required
def note_create_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Catatan '{note.title}' berhasil dibuat.")
            return redirect('notes:note_list')
        else:
            # Menampilkan semua error form jika tidak valid
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{form.fields[field].label if field else ''}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
            # Tetap di halaman form jika error, kirim form dengan error
            context = {
                'title': 'Buat Catatan Baru',
                'form': form  # Form dengan error akan dikirim kembali
            }
            return render(request, 'notes/note_form_page.html', context)
    else:  # GET request
        form = NoteForm()

    context = {
        'title': 'Buat Catatan Baru',
        'form': form
    }
    return render(request, 'notes/note_form_page.html', context)


@login_required
def note_update_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Catatan '{note.title}' berhasil diperbarui.")
            return redirect('notes:note_detail', note_id=note.id)
        else:
            messages.error(request, "Gagal memperbarui catatan. Periksa kembali isian form.")
            # Tetap di halaman form jika error, kirim form dengan error
            context = {
                'title': f'Edit Catatan: {note.title}',
                'form': form,  # Form dengan error
                'note': note
            }
            return render(request, 'notes/note_form_page.html', context)
    else:  # GET request
        form = NoteForm(instance=note)

    context = {
        'title': f'Edit Catatan: {note.title}',
        'form': form,
        'note': note
    }
    return render(request, 'notes/note_form_page.html', context)


@login_required
@require_POST  # <-- DEKORATOR BARU: Memastikan view ini hanya menerima request POST
def note_delete_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)  # Pastikan user hanya bisa hapus catatannya sendiri

    note_title = note.title  # Simpan judul untuk pesan sebelum dihapus
    note.delete()  # Lakukan penghapusan

    messages.success(request, f"Catatan '{note_title}' berhasil dihapus.")
    return redirect('notes:note_list')  # Redirect kembali ke daftar catatan