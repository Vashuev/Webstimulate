from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Entry(models.Model):
    STATUS_CHOICES = [
        ('not_contacted', 'Not Contacted'),
        ('in_progress', 'In Progress'),
        ('completed_interested', 'Completed - Interested'),
        ('appointment_set', 'Appointment Set'),
        ('completed_follow_up_needed', 'Completed - Follow-Up Needed'),
        ('voicemail_left', 'Voicemail Left'),
        ('call_back_later', 'Call Back Later'),
        ('no_answer', 'No Answer'),
        ('wrong_number', 'Wrong Number'),
        ('do_not_call', 'Do Not Call'),
        ('completed_not_interested', 'Completed - Not Interested'),
        ('disconnected_number', 'Disconnected Number'),
    ]

    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    links = models.URLField(blank=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=26, choices=STATUS_CHOICES, default='not_contacted')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_entries')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'number')

    def __str__(self):
        return self.name
