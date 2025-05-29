# SmartLife_Manager_Django/notes/note_logic.py
import uuid # Untuk ID unik sederhana
from datetime import datetime, timezone

def get_notes_from_session(session):
    """Mengambil daftar catatan dari sesi."""
    # Catatan akan disimpan sebagai list of dictionaries
    # {'id': 'uuid_str', 'title': '...', 'content': '...', 'created_at': 'isoformat_str'}
    notes_list_data = session.get('user_notes', [])

    # Konversi kembali string tanggal ke objek datetime untuk konsistensi jika diperlukan
    # (Untuk contoh ini, kita biarkan sebagai string di sesi agar sederhana)
    return notes_list_data

def save_notes_to_session(session, notes_list):
    """Menyimpan daftar catatan ke sesi."""
    session['user_notes'] = notes_list
    session.modified = True

def add_note_to_session(session, title, content):
    """Menambahkan catatan baru ke sesi."""
    notes = get_notes_from_session(session)
    new_note = {
        'id': str(uuid.uuid4()), # ID unik
        'title': title,
        'content': content,
        'created_at': datetime.now(timezone.utc).isoformat() # Simpan sebagai string ISO format
    }
    notes.append(new_note) # Tambah ke akhir list (bisa dianggap paling baru)
    save_notes_to_session(session, notes)
    return new_note

def get_note_by_id_from_session(session, note_id):
    """Mencari catatan berdasarkan ID."""
    notes = get_notes_from_session(session)
    for note in notes:
        if note['id'] == note_id:
            return note
    return None

def update_note_in_session(session, note_id, new_title, new_content):
    """Memperbarui catatan yang ada di sesi."""
    notes = get_notes_from_session(session)
    for i, note in enumerate(notes):
        if note['id'] == note_id:
            notes[i]['title'] = new_title
            notes[i]['content'] = new_content
            notes[i]['updated_at'] = datetime.now(timezone.utc).isoformat() # Tambahkan field updated_at
            save_notes_to_session(session, notes)
            return True
    return False

def delete_note_from_session(session, note_id):
    """Menghapus catatan dari sesi."""
    notes = get_notes_from_session(session)
    notes_after_deletion = [note for note in notes if note['id'] != note_id]
    if len(notes_after_deletion) < len(notes):
        save_notes_to_session(session, notes_after_deletion)
        return True
    return False