from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientRegistrationForm
from .forms import PatientEditForm
from .models import Patient
from django.contrib.auth.hashers import check_password
from appointments.models import Appointment
from django.views import View

# Creer un compte patient
def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Verifier si le mot de passe correspond
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'patients/patient_register.html', {'form': form})

            # Enregistrer le patient dans la base de donnee
            form.save()

            # Rediriger le patient vers la page login
            messages.success(request, 'Votre comptez a ete creer avec succes. Veuillez vous connecter')
            return redirect('patient_login')
        else:
            # Si le formulaire n'est pas valide, affiche le message d'erreur
            messages.error(request, 'Completer toute les lignes requises.')
    else:
        form = PatientRegistrationForm()

    return render(request, 'patients/patient_register.html', {'form': form})

# gestion du patient login
def patient_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Retrouver le patient utilisant l'email
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            # Si l'email n'existe pas dans la BD, on le redirige vers la page login
            messages.error(request, 'Email incorrect.')
            return render(request, 'patients/patient_login.html')

        # Verifier si le mot de passe correspond
        if check_password(password, patient.password):
            # Si le mot de passe est correct
            # You can add additional checks or logic here if needed
            request.session['patient_id'] = patient.id  # On enregistre le patient dans la BD et on le redirige vers le dashboard
            return redirect('patient_dashboard')
        else:
            # Si le mot de passe est incorrect
            messages.error(request, 'mot de passe incorrect') # On renvoie l'erreur et on redirige le patient vers la page login
            return render(request, 'patients/patient_login.html')

    return render(request, 'patients/patient_login.html')

# Gestion de la deconnection du patient
def patient_logout(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
    messages.success(request, 'Vous avez ete deconnecter.')
    return redirect('patient_login')

# Changer les infos du patient
def patient_edit(request):
    patient_id = request.session.get('patient_id')
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
            if request.method == 'POST':
                form = PatientEditForm(request.POST, instance=patient)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Vos informations ont etet modifiees avec succes')
                    return redirect('patient_dashboard')
            else:
                form = PatientEditForm(instance=patient)

            return render(request, 'patients/patient_edit.html', {'form': form, 'patient': patient})
        except Patient.DoesNotExist:
            pass

    messages.error(request, 'Veuillez vous connecter.')
    return redirect('patient_login')

# Gerer le dashboard du patient
def patient_dashboard(request, *args, **kwargs):
    template_name = 'patients/patient_dashboard.html'
    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('patient_login')  #Rediriger le patient vers le login

    patient = Patient.objects.get(id=patient_id)
    
    # voir les consultations passee et ceux avenir
    upcoming_appointments = Appointment.objects.filter(patient=patient, status='Pending')
    past_appointments = Appointment.objects.filter(patient=patient, status__in=['Approved', 'Rejected'])
    
    return render(request, template_name, {'upcoming_appointments': upcoming_appointments, 'past_appointments': past_appointments, 'patient':patient})

def appointment_details(request, appointment_id):
    patient_id = request.session.get('patient_id')
    appointment = get_object_or_404(Appointment, id=appointment_id, patient = Patient.objects.get(id=patient_id))
    return render(request, 'patients/appointment_details.html', {'appointment': appointment})