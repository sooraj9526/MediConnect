from django.db import models
from django.contrib.auth.models import User


# =========================================================
# APPOINTMENT MODEL
# =========================================================

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField(
        help_text="Explain the reason for your appointment"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    doctor_notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.patient.username} - "
            f"Dr. {self.doctor.username} - "
            f"{self.appointment_date}"
        )


# =========================================================
# LAB TEST MODEL
# =========================================================

class LabTest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lab_tests'
    )

    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requested_lab_tests'
    )

    test_name = models.CharField(
        max_length=200
    )

    test_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"{self.test_name} - "
            f"{self.patient.username} - "
            f"{self.status}"
        )


# =========================================================
# LAB REPORT MODEL
# =========================================================

class LabReport(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lab_reports'
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_lab_reports'
    )

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )

    test_name = models.CharField(
        max_length=200
    )

    test_date = models.DateField()

    result = models.TextField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    report_file = models.FileField(
        upload_to='lab_reports/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.test_name} - "
            f"{self.patient.username}"
        )


# =========================================================
# PRESCRIPTION MODEL
# =========================================================

class Prescription(models.Model):

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_prescriptions'
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prescriptions'
    )

    diagnosis = models.TextField(
        blank=True,
        null=True
    )

    instructions = models.TextField(
        blank=True,
        null=True
    )

    prescription_date = models.DateField(
        auto_now_add=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"Prescription - "
            f"{self.patient.username} - "
            f"Dr. {self.doctor.username} - "
            f"{self.prescription_date}"
        )


# =========================================================
# PRESCRIPTION MEDICINE MODEL
# =========================================================

class PrescriptionMedicine(models.Model):

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='medicines'
    )

    medicine_name = models.CharField(
        max_length=200
    )

    dosage = models.CharField(
        max_length=100
    )

    frequency = models.CharField(
        max_length=100
    )

    duration = models.CharField(
        max_length=100
    )

    instructions = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return (
            f"{self.medicine_name} - "
            f"{self.dosage}"
        )