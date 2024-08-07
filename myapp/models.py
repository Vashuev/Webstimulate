from django.db import models
from django.contrib.auth.models import User

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

    CATEGORY_CHOICES = [
        ('local_shops', 'Local Shops and Boutiques'),
        ('online_sellers', 'Online Sellers'),
        ('healthcare', 'Healthcare Providers'),
        ('education', 'Education and Coaching Centers'),
        ('beauty', 'Beauty and Wellness'),
        ('restaurants', 'Restaurants and Cafes'),
        ('hotels', 'Hotels and Guesthouses'),
        ('freelancers', 'Freelancers and Consultants'),
        ('real_estate', 'Real Estate Agents'),
        ('manufacturers', 'Small-scale Manufacturers'),
        ('event_planners', 'Event Planners and Organizers'),
        ('travel_agencies', 'Travel Agencies'),
    ]

    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    links = models.URLField(blank=True)
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=26, choices=STATUS_CHOICES, default='not_contacted')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_entries')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='local_shops')

    def __str__(self):
        return self.name
