from django.db import models
from django.conf import settings # Untuk mengaitkan dengan User
from django.utils import timezone # Untuk default datetime

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'event_time'] # Urutkan berdasarkan tanggal dan waktu

    def __str__(self):
        return f"{self.title} pada {self.event_date.strftime('%d %b %Y')} jam {self.event_time.strftime('%H:%M')}"

    @property
    def is_past_due(self):
        """Mengecek apakah acara sudah lewat (berdasarkan tanggal dan waktu)."""
        event_datetime = datetime.combine(self.event_date, self.event_time)
        # Pastikan event_datetime adalah timezone-aware jika settings.USE_TZ = True
        if timezone.is_naive(event_datetime):
             # Asumsikan waktu lokal server jika naive (sesuaikan jika perlu)
            event_datetime = timezone.make_aware(event_datetime, timezone.get_current_timezone())
        return event_datetime < timezone.now()