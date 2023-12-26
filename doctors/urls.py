# doctors/urls.py
from django.urls import path
from .views import doctor_login, doctor_dashboard, doctor_approve_appointment, doctor_logout, doctor_appointment_details, doctor_video, submit_video_link

urlpatterns = [
    path('login/', doctor_login, name='doctor_login'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('approve-appointment/<int:appointment_id>/', doctor_approve_appointment, name='doctor_approve_appointment'),
    path('doctor_appointment/<int:appointment_id>/', doctor_appointment_details, name='doctor_appointment_details'),
    path('logout/', doctor_logout, name='doctor_logout'),
    path('doctor_video/', doctor_video, name='doctor_video' ),
    path('submit-video-link/<int:appointment_id>/', submit_video_link, name='submit_video_link')
]