from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # Digunakan oleh UserCreationForm dan sebagai model di Meta


class CustomUserCreationForm(UserCreationForm):
    # Mendefinisikan field email secara eksplisit untuk membuatnya required dan kustomisasi widget
    email = forms.EmailField(
        required=True,
        label="Alamat Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan alamat email Anda',  # Placeholder yang lebih deskriptif
            'id': 'email'  # ID untuk JavaScript jika diperlukan
        })
    )

    # Komentar Anda untuk first_name dan last_name sudah baik jika ingin menambahkannya nanti
    # first_name = forms.CharField(required=False, label="Nama Depan", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Depan'}))
    # last_name = forms.CharField(required=False, label="Nama Belakang", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Belakang'}))

    class Meta(UserCreationForm.Meta):
        model = User
        # Menyertakan field standar dari UserCreationForm dan menambahkan 'email'
        # Jika Anda menambahkan first_name dan last_name, sertakan juga di sini:
        # fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        fields = UserCreationForm.Meta.fields + ('email',)

        # Mengkustomisasi widget untuk field 'username' yang diwarisi dari UserCreationForm
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pilih username unik',
                'id': 'username',
                'required': True  # Atribut HTML5 untuk validasi sisi klien
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mengkustomisasi label dan widget untuk field password yang diwarisi
        # Ini cara yang baik untuk memastikan field bawaan sesuai dengan desain Anda

        if 'username' in self.fields:  # Memberikan label yang konsisten
            self.fields['username'].label = "Username"

        if 'password1' in self.fields:  # 'password1' adalah field password utama
            self.fields['password1'].label = "Password"
            self.fields['password1'].help_text = None  # Menghilangkan help_text default jika ada dan tidak diinginkan
            self.fields['password1'].widget = forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan password Anda',
                'id': 'password',  # Untuk JS password strength
                'required': True
            })
        if 'password2' in self.fields:  # 'password2' adalah field konfirmasi password
            self.fields['password2'].label = "Konfirmasi Password"
            self.fields['password2'].help_text = None  # Menghilangkan help_text default jika ada
            self.fields['password2'].widget = forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ketik ulang password Anda',
                'id': 'confirmPassword',  # Untuk JS password match
                'required': True
            })


class CustomAuthenticationForm(AuthenticationForm):
    # Mengkustomisasi widget untuk field username dan password dari AuthenticationForm
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username Anda',
            'id': 'username',
            'autofocus': True  # Otomatis fokus ke field ini saat halaman dimuat
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password Anda',
            'id': 'password'
        })
    )