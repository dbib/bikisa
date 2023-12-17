from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Doctor
from django.views import View
from appointments.models import Appointment

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if check_password(password, doctor.password):
                # Password is correct, log in the user
                request.session['doctor_id'] = doctor.id  # Enregistrer les donnees du medecin dans la  session
                return redirect('doctor_dashboard')
            else:
                # Password is incorrect
                messages.error(request, 'Email ou mot de passe incorrecte.')
        except Doctor.DoesNotExist:
            # Email does not exist in the database
            messages.error(request, 'Email ou mot de passe incorrecte')

    return render(request, 'doctors/doctor_login.html')

# Gerer le dashboards de medecins le @ assure que vous devez etre connecter pour avoir acces a cette page
def doctor_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_email' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect('page_does_not_exist')
        
        user_email = request.session['user_email']
        
        try:
            doctor = Doctor.objects.get(email=user_email)
        except Doctor.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('page_does_not_exist')
        

        return view_func(request, doctor, *args, **kwargs)
    
    return _wrapped_view

# gerer la deconnexion du medecin
def doctor_logout(request):
    # Effacer les donnees de la session
    if 'user_email' in request.session:
        del request.session['user_email']
        messages.success(request, 'You have been successfully logged out.')
    
    return redirect('doctor_login')

# Gerer le dashboard du medecin
def doctor_dashboard(request, *args, **kwargs):
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        messages.error(request, "vous devez vous connecter")
        return redirect('doctor_login')  # Redirect to the doctor login page with a "Please login" message

    doctor = Doctor.objects.get(id=doctor_id)
    pending_appointments = Appointment.objects.filter(doctor=doctor, status="Pending")
    
    return render(request, 'doctors/doctor_dashboard.html', {'pending_appointments': pending_appointments})

# Gerer les consultations accepter ou autoriser
def doctor_approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            appointment.status = 'Approved'
        elif action == 'reject':
            appointment.status = 'Rejected'

        appointment.save()

    return redirect('doctor_dashboard')