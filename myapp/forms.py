from django import forms
from django.contrib.auth.models import User
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'place', 'number', 'links', 'remarks', 'status', 'assigned_to']

class EntryUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name', 'place', 'links', 'remarks', 'status',]



class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV file')
    assigned_user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), label='Assign to User')
