from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class DoctorManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        doctor = self.model(email=email, name=name)
        doctor.set_password(password)
        doctor.save(using=self._db)
        return doctor

    def create_superuser(self, email, name, password=None):
        doctor = self.create_user(email, name, password)
        doctor.is_admin = True
        doctor.save(using=self._db)
        return doctor

class Doctor(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctor_profile_pics/', default='doctor_profile_pics/default.png')
    hospital = models.CharField(max_length=255, default='Docs')
    creator = models.CharField(max_length=255, default='manager1')

    is_admin = models.BooleanField(default=False)

    objects = DoctorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} -- {self.hospital}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
