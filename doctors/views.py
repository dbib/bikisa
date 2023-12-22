from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import Doctor
from django.views import View
from appointments.models import Appointment

def doctor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(email=email)
            if password == doctor.password:
            #if check_password(password, doctor.password):
                # Si le mot de passe est correct, on enregistre l'utilisateur dans la session
                request.session['doctor_id'] = doctor.id  # Enregistrer les donnees du medecin dans la  session
                return redirect('doctor_dashboard')
            else:
                # Si le mot de passe est incorrect
                messages.error(request, 'Email ou mot de passe incorrecte.')
        except Doctor.DoesNotExist:
            # Si l'email n'existe pas dans la base de donnee
            messages.error(request, 'Email ou mot de passe incorrecte')

    return render(request, 'doctors/doctor_login.html')

# Gerer le dashboards de medecins 
def doctor_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_email' not in request.session:
            messages.error(request, 'Connecter vous pour acceder a la page')
            return redirect("La page n'existe pas")
        
        user_email = request.session['user_email']
        
        try:
            doctor = Doctor.objects.get(email=user_email)
        except Doctor.DoesNotExist:
            messages.error(request, "L'utilisateur n'existe pas")
            return redirect("La page n'existe pas")
        

        return view_func(request, doctor, *args, **kwargs)
    
    return _wrapped_view

# gerer la deconnexion du medecin
def doctor_logout(request):
    # Effacer les donnees de la session
    if 'user_email' in request.session:
        del request.session['user_email']
        messages.success(request, "Vous avez ete deconnecter avec succes")
    
    return redirect('doctor_login')

# Gerer le dashboard du medecin
def doctor_dashboard(request, *args, **kwargs):
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        messages.error(request, "vous devez vous connecter")
        return redirect('doctor_login')  # Rediriger vers la page login de medecin
    
    # Recuperer les donnees du medecin, les demandes de consultation et la liste des consultation approuver mais dans le futur
    doctor = Doctor.objects.get(id=doctor_id)
    pending_appointments = Appointment.objects.filter(doctor=doctor, status="Pending")
    approved_appointments = Appointment.objects.filter(doctor=doctor, status= 'Approved')
    
    return render(request, 'doctors/doctor_dashboard.html', {'pending_appointments': pending_appointments, 'approved_appointments': approved_appointments, 'doctor': doctor})

# Gerer les consultations accepter ou autoriser
def doctor_approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            appointment.status = 'Approved'
            messages.success(request, f'Votre demande de consultation #{appointment_id} a ete approuver.')
        elif action == 'reject':
            appointment.status = 'Rejected'
            messages.warning(request, f'Votre demande de consultation #{appointment_id} a ete rejetter.')

        appointment.save()
        
        JsonResponse({'status': 'success'})

    return redirect('doctor_dashboard')

# Gerer les details des consultation
def doctor_appointment_details(request, appointment_id):
    doctor = Doctor.objects.get(id=request.session.get('doctor_id'))
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    return render(request, 'doctors/appointment_details.html', {'appointment': appointment})
    
# Gerer les appels videos
def doctor_video(request):
    doctor_id = request.session.get('doctor_id')
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'doctors/doctor_video.html', {'doctor': doctor})