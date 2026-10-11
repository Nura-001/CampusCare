from django.conf import settings
from django.db import models


class ComplaintCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'complaint categories'

    def __str__(self):
        return self.name


class Complaint(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        URGENT = 4, 'Urgent'

    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        UNDER_REVIEW = 'under_review', 'Under Review'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        REJECTED = 'rejected', 'Rejected'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='complaints',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        ComplaintCategory,
        on_delete=models.PROTECT,
        related_name='complaints',
    )
    location = models.CharField(max_length=150)
    room_number = models.CharField(max_length=30, blank=True)
    priority = models.IntegerField(
        choices=Priority.choices, default=Priority.MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SUBMITTED
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints',
        limit_choices_to={'is_staff': True},
    )
    admin_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.pk} {self.title}'


class ComplaintHistory(models.Model):
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='history',
    )
    previous_status = models.CharField(
        max_length=20, choices=Complaint.Status.choices, blank=True
    )
    new_status = models.CharField(
        max_length=20, choices=Complaint.Status.choices
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='status_changes',
    )
    remarks = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'complaint history'

    def __str__(self):
        return f'{self.complaint_id}: {self.previous_status} -> {self.new_status}'