from django.urls import path
from django.urls import reverse_lazy
from . import views

app_name = 'appointments'

urlpatterns = [
    path('create/', views.appointment_create, name='appointment_create'),
    # Add other URL patterns as needed
]