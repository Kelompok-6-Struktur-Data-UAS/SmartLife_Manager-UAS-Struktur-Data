from django.db import models
from django.conf import settings  # Untuk mengaitkan dengan User
from django.utils import timezone  # Untuk default datetime dan fungsi timezone
from datetime import datetime  # <--- PASTIKAN IMPORT INI ADA


class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedule_events'  # related_name yang baik untuk akses dari objek user
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)  # Menggunakan timezone.now untuk datetime yang aware
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date', 'event_time']  # Urutkan berdasarkan tanggal dan waktu

    def __str__(self):
        # Format string yang lebih aman jika field tanggal/waktu mungkin None
        # (meskipun model saat ini mengharuskannya, ini praktik defensif)
        date_str = self.event_date.strftime('%d %b %Y') if self.event_date else "Tanggal tidak ada"
        time_str = self.event_time.strftime('%H:%M') if self.event_time else "Waktu tidak ada"
        return f"{self.title} pada {date_str} jam {time_str}"

    @property
    def is_past_due(self):
        """
        Mengecek apakah acara sudah lewat (berdasarkan tanggal dan waktu acara).
        Membandingkan dengan waktu saat ini yang sudah timezone-aware.
        """
        if not self.event_date or not self.event_time:
            return False  # Tidak bisa menentukan jika tanggal atau waktu tidak ada

        # Gabungkan tanggal dan waktu acara menjadi objek datetime
        # datetime.combine menghasilkan naive datetime, jadi kita perlu membuatnya aware
        # jika USE_TZ=True di settings.py (yang merupakan default dan praktik baik).
        naive_event_datetime = datetime.combine(self.event_date, self.event_time)

        # Dapatkan zona waktu saat ini yang digunakan oleh Django
        # (berdasarkan setting TIME_ZONE Anda atau UTC jika tidak diset spesifik)
        current_tz = timezone.get_current_timezone()
        aware_event_datetime = timezone.make_aware(naive_event_datetime, current_tz)

        # timezone.now() sudah mengembalikan datetime yang aware
        return aware_event_datetime < timezone.now()
