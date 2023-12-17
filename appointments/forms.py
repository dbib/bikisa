from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
from doctors.models import Doctor
from patients.models import Patient

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'appointment_time', 'reason']

    doctor = forms.ModelChoiceField(
        label='Medecin',
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    appointment_date = forms.DateField(
        label="Veuillez choisir la date",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    appointment_time = forms.TimeField(
        label="Veuillez choisir l'heure",
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label="Comment vous sentez vous"
    )

    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        super().__init__(*args, **kwargs)

        # Set the initial value for the doctor field queryset
        self.fields['doctor'].queryset = Doctor.objects.all()  # Replace Doctor with your actual Doctor model

        # Set the initial value for the patient field
        if patient_id:
            try:
                patient = Patient.objects.get(id=patient_id)
                self.fields['patient'].initial = patient
            except Patient.DoesNotExist:
                raise ValidationError("Le patient n'existe pas")

    def save(self, commit=True):
        instance = super(AppointmentForm, self).save(commit=False)
        instance.patient = Patient.objects.get(id=self.initial.get('patient'))
        instance.date = self.cleaned_data['appointment_date']
        instance.time = self.cleaned_data['appointment_time']
        
        if commit:
            instance.save()

        return instance