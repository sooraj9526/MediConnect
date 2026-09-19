from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('lab_technician', 'Lab Technician'),
        ('receptionist', 'Receptionist'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"