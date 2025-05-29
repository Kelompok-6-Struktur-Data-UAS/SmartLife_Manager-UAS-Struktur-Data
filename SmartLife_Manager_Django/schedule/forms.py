from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    # Menggunakan DateInput dan TimeInput untuk input type="date" dan type="time" di HTML
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Tanggal Acara"
    )
    event_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label="Waktu Acara"
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Meeting Tim Proyek'}),
        label="Judul Acara"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deskripsi singkat mengenai acara...'}),
        required=False, # Deskripsi tidak wajib
        label="Deskripsi (Opsional)"
    )
    location = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Ruang Rapat A / Online'}),
        required=False, # Lokasi tidak wajib
        label="Lokasi (Opsional)"
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'event_time', 'location']