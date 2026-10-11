from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ComplaintForm
from .models import Complaint, ComplaintHistory


@login_required
def complaint_list(request):
    complaints = (
        Complaint.objects
        .filter(student=request.user)
        .select_related('category')
    )
    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(
        Complaint.objects.select_related('category', 'assigned_to'),
        pk=pk,
        student=request.user,
    )
    history = complaint.history.select_related('changed_by')
    return render(
        request,
        'complaints/complaint_detail.html',
        {'complaint': complaint, 'history': history},
    )


@login_required
def complaint_create(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                complaint = form.save(commit=False)
                complaint.student = request.user
                complaint.save()
                ComplaintHistory.objects.create(
                    complaint=complaint,
                    previous_status='',
                    new_status=complaint.status,
                    changed_by=request.user,
                    remarks='Complaint submitted.',
                )
            messages.success(request, 'Your complaint has been submitted.')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintForm()

    return render(request, 'complaints/complaint_form.html', {'form': form})


@login_required
def complaint_edit(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, student=request.user)

    if complaint.status != Complaint.Status.SUBMITTED:
        messages.error(request, 'You can only edit a complaint while its status is Submitted.')
        return redirect('complaints:detail', pk=complaint.pk)

    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your complaint has been updated.')
            return redirect('complaints:detail', pk=complaint.pk)
    else:
        form = ComplaintForm(instance=complaint)

    return render(
        request,
        'complaints/complaint_form.html',
        {'form': form, 'is_edit': True, 'complaint': complaint},
    )


@login_required
def complaint_delete(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, student=request.user)

    if complaint.status != Complaint.Status.SUBMITTED:
        messages.error(request, 'You can only delete a complaint while its status is Submitted.')
        return redirect('complaints:detail', pk=complaint.pk)

    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Your complaint has been deleted.')
        return redirect('complaints:list')

    return render(request, 'complaints/complaint_confirm_delete.html', {'complaint': complaint})