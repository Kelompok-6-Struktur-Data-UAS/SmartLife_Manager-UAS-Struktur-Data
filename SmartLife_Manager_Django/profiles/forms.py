from django import forms
from django.contrib.auth.models import User # Menggunakan User model bawaan

class UserProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label="Alamat Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@contoh.com'})
    )
    first_name = forms.CharField(
        label="Nama Depan",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama depan Anda'})
    )
    last_name = forms.CharField(
        label="Nama Belakang",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama belakang Anda'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']