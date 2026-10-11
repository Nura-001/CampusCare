from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra information for each user. One user has one profile."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    full_name = models.CharField(max_length=150)
    student_id = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.full_name or self.user.username
