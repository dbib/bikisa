from django.shortcuts import render, redirect
from django.contrib import messages
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
            # Check if passwords match
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'patients/patient_register.html', {'form': form})

            # Save the patient to the database
            form.save()

            # Redirect to the patient login page
            messages.success(request, 'Votre comptez a ete creer avec succes. Veuillez vous connecter')
            return redirect('patient_login')
        else:
            # Form is not valid, display an error message
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
            # Retrieve patient with the given email
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            # Patient with the given email does not exist
            messages.error(request, 'Email ou mot de passe incorrect.')
            return render(request, 'patients/patient_login.html')

        # Check if the provided password matches the stored hashed password
        if check_password(password, patient.password):
            # Password is correct
            # You can add additional checks or logic here if needed
            request.session['patient_id'] = patient.id  # Store patient ID in the session
            return redirect('patient_dashboard')
        else:
            # Password is incorrect
            messages.error(request, 'Email ou mot de passe incorrect')
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
                    messages.success(request, 'Your information has been updated.')
                    return redirect('patient_dashboard')
            else:
                form = PatientEditForm(instance=patient)

            return render(request, 'patients/patient_edit.html', {'form': form, 'patient': patient})
        except Patient.DoesNotExist:
            pass

    messages.error(request, 'Please log in first.')
    return redirect('patient_login')

# Gerer le dashboard du patient
def patient_dashboard(request, *args, **kwargs):
    template_name = 'patients/patient_dashboard.html'
    patient_id = request.session.get('patient_id')

    if not patient_id:
        return redirect('patient_login')  # Redirect to the patient login page with a "Please login" message

    patient = Patient.objects.get(id=patient_id)
    
    # voir les consultation passee et ceux avenir
    upcoming_appointments = Appointment.objects.filter(patient=patient, status='Pending')
    past_appointments = Appointment.objects.filter(patient=patient, status__in=['Approved', 'Rejected'])
    
    return render(request, template_name, {'upcoming_appointments': upcoming_appointments, 'past_appointments': past_appointments, 'patient':patient})