from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    title = forms.CharField(
        label="Judul Catatan",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg', # Kelas Bootstrap untuk input besar
            'placeholder': 'Masukkan judul catatan...'
        })
    )
    content = forms.CharField(
        label="Isi Catatan",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10, # Jumlah baris awal textarea
            'placeholder': 'Tulis catatan Anda di sini...'
        })
    )

    class Meta:
        model = Note
        fields = ['title', 'content']