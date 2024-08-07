# appointments/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from .google_calendar import add_appointment_to_google_calendar, get_user_busy_events
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def create_appointment(request):
    attendees = request.POST.get('attendees', '')
    appointment_data = {
        'title': request.POST.get('summary'),
        'description': request.POST.get('description'),
        'start_time': request.POST.get('start'),
        'end_time': request.POST.get('end'),
    }

    attendee_emails = [email.strip() for email in attendees.split(',')] if attendees else []
    created_event = add_appointment_to_google_calendar(request.user.email, appointment_data, attendee_emails)

    return JsonResponse({'status': 'success', 'event': created_event})



@login_required
def user_appointment_view(request):
    user_email = request.user.email
    user_events, busy_events = get_user_busy_events(user_email)
    context = {
        'user_events': user_events,
        'busy_events': busy_events,
    }
    return render(request, 'user_appointment.html', context)