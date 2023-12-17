from django import forms
from .models import Patient

class PatientRegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password',
        required=True
    )

    class Meta:
        model = Patient
        fields = ['full_name', 'email', 'phone_number', 'address', 'profile_image', 'birth_date', 'password']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required except for profile_image
        for field_name, field in self.fields.items():
            if field_name != 'profile_image':
                field.required = True

    def save(self, commit=True):
        # Save the hashed password
        patient = super().save(commit=False)
        patient.set_password(self.cleaned_data['password'])
        if commit:
            patient.save()
        return patient

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'email', 'phone_number', 'address', 'profile_image', 'birth_date']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }