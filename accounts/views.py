from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from complaints.models import Complaint

from .forms import StudentRegistrationForm


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to CampusCare! Your account has been created.')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    complaints = Complaint.objects.filter(student=request.user)
    S = Complaint.Status
    counts = complaints.aggregate(
        total=Count('id'),
        submitted=Count('id', filter=Q(status=S.SUBMITTED)),
        under_review=Count('id', filter=Q(status=S.UNDER_REVIEW)),
        in_progress=Count('id', filter=Q(status=S.IN_PROGRESS)),
        resolved=Count('id', filter=Q(status=S.RESOLVED)),
    )
    recent = complaints.select_related('category')[:5]
    return render(request, 'dashboard/student_dashboard.html', {
        'counts': counts,
        'recent': recent,
    })