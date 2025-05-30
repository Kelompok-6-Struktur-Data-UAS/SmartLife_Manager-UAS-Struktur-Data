from django import forms
from .models import Goal, SubTask

class GoalForm(forms.ModelForm):
    title = forms.CharField(label="Judul Tujuan", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Belajar Django Tingkat Lanjut'}))
    description = forms.CharField(label="Deskripsi Tujuan", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detail mengenai tujuan Anda...'}))
    priority = forms.IntegerField(label="Prioritas (0-10)", min_value=0, max_value=10, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    due_date = forms.DateField(label="Tanggal Target Selesai (Opsional)", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    is_completed = forms.BooleanField(label="Sudah Selesai?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = Goal
        fields = ['title', 'description', 'priority', 'due_date', 'is_completed']

class SubTaskForm(forms.ModelForm):
    title = forms.CharField(label="Judul Sub-Tugas", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Baca dokumentasi Models'}))
    description = forms.CharField(label="Deskripsi Sub-Tugas", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detail sub-tugas...'}))
    priority = forms.IntegerField(label="Prioritas Sub-Tugas (0-10)", min_value=0, max_value=10, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    is_completed = forms.BooleanField(label="Sudah Selesai?", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    # 'goal' akan di-set di view

    class Meta:
        model = SubTask
        fields = ['title', 'description', 'priority', 'is_completed']