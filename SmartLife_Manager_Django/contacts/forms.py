from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label="Nama Kontak",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama lengkap'})
    )
    email = forms.EmailField(
        label="Alamat Email",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contoh@email.com'})
    )
    phone_number = forms.CharField(
        label="Nomor Telepon",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0812xxxxxxxx'})
    )
    relationship_type = forms.CharField(
        label="Jenis Relasi",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teman, Keluarga, dll.'})
    )
    birthday = forms.DateField(
        label="Tanggal Lahir",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    last_interaction_date = forms.DateField(
        label="Interaksi Terakhir",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    notes = forms.CharField(
        label="Catatan Tambahan",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Info penting tentang kontak ini...'})
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'relationship_type', 'birthday', 'last_interaction_date', 'notes']