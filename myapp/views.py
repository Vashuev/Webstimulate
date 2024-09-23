from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Entry
from .forms import EntryForm, EntryUpdateForm
from django.http import HttpResponseForbidden
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.paginator import Paginator

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})





@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    entries = Entry.objects.all()

    users = User.objects.filter(is_staff=False)  # Get all non-admin users

    positive_statuses = [
        'completed_interested', 'appointment_set', 'in_progress'
    ]
    neutral_statuses = [
        'not_contacted', 'completed_follow_up_needed', 'voicemail_left', 'call_back_later', 'no_answer'
    ]
    negative_statuses = [
        'wrong_number', 'do_not_call', 'completed_not_interested', 'disconnected_number'
    ]

    user_data = []
    for user in users:
        user_entries = Entry.objects.filter(assigned_to=user)
        status_counts = {
            'positive': {status: user_entries.filter(status=status).count() for status in positive_statuses},
            'neutral': {status: user_entries.filter(status=status).count() for status in neutral_statuses},
            'negative': {status: user_entries.filter(status=status).count() for status in negative_statuses},
            'not_contacted': user_entries.filter(status='not_contacted').count()
        }
        user_data.append({
            'user': user,
            'status_counts': status_counts,
        })

    context = {
        'entries': entries,
        'user_data': user_data,
        'positive_statuses': positive_statuses,
        'neutral_statuses': neutral_statuses,
        'negative_statuses': negative_statuses
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def user_dashboard(request,  user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
        entries = Entry.objects.filter(assigned_to=user)
    else:
        entries = Entry.objects.filter(assigned_to=request.user)
    status_filter = request.GET.get('status_filter')

    if status_filter:
        entries = entries.filter(status=status_filter)

    paginator = Paginator(entries, 20)  # Show 20 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'entries': page_obj,
        'status_choices': Entry.STATUS_CHOICES,
        'username': request.user.username,
    }
    return render(request, 'user_dashboard.html', context)



@login_required
def update_entry(request, pk):
    entry = get_object_or_404(Entry, id=pk)
    if request.user != entry.assigned_to and not request.user.is_staff:
        return redirect('user_dashboard')

    form = EntryUpdateForm(instance=entry)

    if request.method == 'POST':
        form = EntryUpdateForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')

    context = {
        'form': form,
        'entry': entry,
    }
    return render(request, 'update_entry.html', context)


@login_required
def update_user_remarks(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.user != entry.assigned_to and not request.user.is_staff:
        return redirect('user_dashboard')

    if request.method == 'POST':
        entry.remarks = request.POST.get('remarks')
        entry.save()
        return redirect('user_dashboard')

@login_required
def update_user_status(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.user != entry.assigned_to and not request.user.is_staff:
        return redirect('user_dashboard')

    if request.method == 'POST':
        # Update the status
        status = request.POST.get('status')
        entry.status = status
        entry.save()

        # Check if the status is "Appointment Set"
        if status == 'appointment_set':
            return redirect('user_appointment')

        # Otherwise, redirect to the user dashboard
        return redirect('user_dashboard')
