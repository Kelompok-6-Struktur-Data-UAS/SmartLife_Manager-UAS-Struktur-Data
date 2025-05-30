from django.db import models
from django.conf import settings
from django.utils import timezone

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts_list') # related_name diubah agar unik
    name = models.CharField(max_length=100, verbose_name="Nama Kontak")
    email = models.EmailField(max_length=254, blank=True, null=True, verbose_name="Alamat Email")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor Telepon")
    relationship_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Jenis Relasi",
        help_text="Contoh: Teman, Keluarga, Rekan Kerja"
    )
    birthday = models.DateField(blank=True, null=True, verbose_name="Tanggal Lahir")
    last_interaction_date = models.DateField(blank=True, null=True, verbose_name="Interaksi Terakhir")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan Tambahan")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name'] # Urutkan berdasarkan nama kontak

    def __str__(self):
        return self.name