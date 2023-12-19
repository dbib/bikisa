from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import AppointmentForm

def appointment_create(request, *args, **kwargs):
    template_name = 'appointments/appointment_create.html'

    if request.method == 'POST':
        form = AppointmentForm(request.POST or None, initial={'patient': request.session.get('patient_id')})

        if form.is_valid():
            try:
                # Enregistrer une demande de consultation avec un etat "en attente"
                appointment = form.save(commit=True)
                
                return redirect('patient_dashboard')  # Rediriger les patients vers le dashboard patient
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, template_name, {'form': form})
    else:
        form = AppointmentForm(initial={'patient': request.session.get('patient_id')})

    return render(request, template_name, {'form': form})


