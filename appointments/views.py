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
                # Save the appointment in a pending state
                appointment = form.save(commit=True)

                # Add any additional logic, such as sending notifications

                return redirect('patient_dashboard')  # Redirect to the patient dashboard after appointment request
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, template_name, {'form': form})
    else:
        form = AppointmentForm(initial={'patient': request.session.get('patient_id')})

    return render(request, template_name, {'form': form})