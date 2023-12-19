# doctors/urls.py
from django.urls import path
from .views import doctor_login, doctor_dashboard, doctor_approve_appointment, doctor_logout, appointment_details

urlpatterns = [
    path('login/', doctor_login, name='doctor_login'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('approve-appointment/<int:appointment_id>/', doctor_approve_appointment, name='doctor_approve_appointment'),
    path('appointments/<int:appointment_id>/', appointment_details, name='appointment_details'),
    path('logout/', doctor_logout, name='doctor_logout'),
]