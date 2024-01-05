from django.db import models
from datetime import date
from doctors.models import Doctor
from patients.models import Patient

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Hospitalized','Hospitalized'),
        ('Finished','Finished'),
    ]
    
    NOTIFICATION_CHOICES = [
        ('Not Sent', 'Not Sent'),
        ('Sent', 'Sent')
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    time = models.TimeField(default='12:00:00')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    video_link = models.URLField(blank=True, default='empty')
    notification_status = models.CharField(
        max_length=20,
        choices=NOTIFICATION_CHOICES,
        default='Not Sent',
    )

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.date} {self.time}"