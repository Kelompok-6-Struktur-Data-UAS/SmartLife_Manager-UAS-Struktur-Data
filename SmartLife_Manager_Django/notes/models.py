from django.db import models
from django.conf import settings # Untuk mengaitkan dengan User
from django.utils import timezone # Untuk default datetime

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] # Urutkan berdasarkan yang terakhir diupdate tampil duluan

    def __str__(self):
        return self.title