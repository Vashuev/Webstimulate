from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'place', 'number', 'links', 'remarks', 'status', 'assigned_to']

class EntryUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'place', 'links', 'remarks', 'status',]
