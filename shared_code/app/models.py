from django.db import models
from django.utils import timezone
from datetime import timedelta

class SharedCode(models.Model):
    text = models.TextField()
    pin = models.CharField(max_length=4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        now = timezone.now()
        expire_time = self.created_at + timedelta(hours=24)
        return now > expire_time

    def __str__(self):
        return f"PIN: {self.pin}"