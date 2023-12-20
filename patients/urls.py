from django.urls import path
from .views import home, patient_register, patient_login, patient_dashboard, patient_logout, patient_edit, appointment_details

urlpatterns = [
    path('', home, name='home'),
    path('register/', patient_register, name='patient_register'),
    path('login/', patient_login, name='patient_login'),
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
    path('logout/', patient_logout, name='patient_logout'),
    path('edit/', patient_edit, name='patient_edit'),
    path('appointments/<int:appointment_id>/', appointment_details, name='appointment_details'),
]