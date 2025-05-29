# SmartLife_Manager_Django/tasks/forms.py
from django import forms

class AddTaskForm(forms.Form):
    task_description = forms.CharField(
        label='Deskripsi Tugas Baru',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan tugas baru...'})
    )