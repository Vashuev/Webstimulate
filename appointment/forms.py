# appointments/forms.py

from django import forms

class AppointmentForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    attendees = forms.CharField(widget=forms.Textarea, help_text='Enter attendee emails, separated by commas.')
