from django.db import models
from django.conf import settings
from django.utils import timezone

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255, verbose_name="Judul Tujuan")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    priority = models.IntegerField(default=0, help_text="Semakin tinggi angka, semakin tinggi prioritas", verbose_name="Prioritas")
    due_date = models.DateField(blank=True, null=True, verbose_name="Tanggal Target Selesai")
    is_completed = models.BooleanField(default=False, verbose_name="Sudah Selesai")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'due_date', 'title'] # Prioritas tertinggi, lalu tanggal terdekat

    def __str__(self):
        return self.title

    def get_progress_percentage(self):
        total_subtasks = self.subtasks.count()
        if total_subtasks == 0:
            return 100 if self.is_completed else 0
        completed_subtasks = self.subtasks.filter(is_completed=True).count()
        return int((completed_subtasks / total_subtasks) * 100) if total_subtasks > 0 else 0

class SubTask(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=255, verbose_name="Judul Sub-Tugas")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Sub-Tugas")
    priority = models.IntegerField(default=0, help_text="Prioritas relatif dalam tujuan ini")
    is_completed = models.BooleanField(default=False, verbose_name="Selesai")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['goal', '-priority', 'created_at']

    def __str__(self):
        return f"{self.title} (untuk Tujuan: {self.goal.title})"