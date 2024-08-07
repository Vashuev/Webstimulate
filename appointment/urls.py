# appointments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('user_appointment_view/', views.user_appointment_view, name='user_appointment'),
]
