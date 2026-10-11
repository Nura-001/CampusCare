from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import Count
from django.shortcuts import render

from complaints.models import Complaint


@staff_member_required
def staff_dashboard(request):
    status_counts = Complaint.objects.aggregate(
        submitted=Count(
            'id',
            filter=models.Q(status=Complaint.Status.SUBMITTED)
        ),
        under_review=Count(
            'id',
            filter=models.Q(status=Complaint.Status.UNDER_REVIEW)
        ),
        in_progress=Count(
            'id',
            filter=models.Q(status=Complaint.Status.IN_PROGRESS)
        ),
        resolved=Count(
            'id',
            filter=models.Q(status=Complaint.Status.RESOLVED)
        ),
        rejected=Count(
            'id',
            filter=models.Q(status=Complaint.Status.REJECTED)
        ),
    )

    context = {
        'total_complaints': Complaint.objects.count(),
        'status_counts': status_counts,
    }

    return render(request, 'adminpanel/dashboard.html', context)
