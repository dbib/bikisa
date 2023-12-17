from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class PatientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('une addresse mail doit etre defini')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)

class Patient(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='patient_profile_pics/', default='patient_profile_pics/default.png')
    birth_date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=128)
    appointments = models.ManyToManyField('appointments.Appointment', related_name='patient_appointments')

    # Add other relevant fields as needed

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PatientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    # Add related_name to avoid clashes with auth.User's groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='patient_set',
        related_query_name='patient',
        blank=True,
        verbose_name='groups',
        help_text='The groups this patient belongs to. A patient will get all permissions granted to '
                  'their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='patient_set',
        related_query_name='patient',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this patient.',
    )

    def __str__(self):
        return self.email
    
    