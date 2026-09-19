from django import forms
from django.contrib.auth.models import User

from .models import (
    Appointment,
    LabTest,
    LabReport,
    Prescription,
    PrescriptionMedicine
)


# =========================================================
# APPOINTMENT FORM
# =========================================================

class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment

        fields = [
            'doctor',
            'appointment_date',
            'appointment_time',
            'reason'
        ]

        widgets = {
            'doctor': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'appointment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'appointment_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Explain the reason for your appointment'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['doctor'].queryset = User.objects.filter(
            userprofile__role='doctor'
        )


# =========================================================
# LAB TEST FORM
# =========================================================

class LabTestForm(forms.ModelForm):

    class Meta:
        model = LabTest

        fields = [
            'test_name',
            'test_date',
            'notes'
        ]

        widgets = {

            'test_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter laboratory test name'
                }
            ),

            'test_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter any additional notes'
                }
            ),
        }

        labels = {
            'test_name': 'Laboratory Test',
            'test_date': 'Test Date',
            'notes': 'Additional Notes'
        }


# =========================================================
# DOCTOR - REQUEST LABORATORY TEST
# =========================================================

class LabTestRequestForm(forms.ModelForm):

    patient = forms.ModelChoiceField(
        queryset=User.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
        empty_label='Select Patient'
    )

    class Meta:
        model = LabTest

        fields = [
            'patient',
            'test_name',
            'test_date',
            'notes'
        ]

        widgets = {

            'test_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Blood Test, CBC, Lipid Profile'
                }
            ),

            'test_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter instructions or additional notes'
                }
            ),
        }

        labels = {
            'patient': 'Patient',
            'test_name': 'Laboratory Test',
            'test_date': 'Test Date',
            'notes': 'Additional Notes'
        }

    def __init__(self, *args, **kwargs):

        doctor = kwargs.pop('doctor', None)

        super().__init__(*args, **kwargs)

        if doctor:

            self.fields['patient'].queryset = User.objects.filter(
                patient_appointments__doctor=doctor,
                userprofile__role='patient'
            ).distinct().order_by(
                'username'
            )


# =========================================================
# LAB REPORT FORM
# =========================================================

class LabReportForm(forms.ModelForm):

    class Meta:
        model = LabReport

        fields = [
            'lab_test',
            'result',
            'notes',
            'report_file'
        ]

        widgets = {

            'lab_test': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'result': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter the laboratory test result'
                }
            ),

            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter additional notes'
                }
            ),

            'report_file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

        labels = {
            'lab_test': 'Completed Laboratory Test',
            'result': 'Test Result',
            'notes': 'Additional Notes',
            'report_file': 'Upload Report File'
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['lab_test'].queryset = LabTest.objects.filter(
            status='completed'
        ).order_by(
            '-updated_at'
        )


# =========================================================
# PRESCRIPTION FORM
# =========================================================

class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription

        fields = [
            'patient',
            'appointment',
            'diagnosis',
            'instructions'
        ]

        widgets = {

            'patient': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'appointment': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'diagnosis': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter patient diagnosis'
                }
            ),

            'instructions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter general instructions for the patient'
                }
            ),
        }

        labels = {
            'patient': 'Patient',
            'appointment': 'Appointment',
            'diagnosis': 'Diagnosis',
            'instructions': 'General Instructions'
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['patient'].queryset = User.objects.filter(
            userprofile__role='patient'
        ).order_by(
            'username'
        )

        self.fields['appointment'].required = False


# =========================================================
# PRESCRIPTION MEDICINE FORM
# =========================================================

class PrescriptionMedicineForm(forms.ModelForm):

    class Meta:
        model = PrescriptionMedicine

        fields = [
            'medicine_name',
            'dosage',
            'frequency',
            'duration',
            'instructions'
        ]

        widgets = {

            'medicine_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Paracetamol'
                }
            ),

            'dosage': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 500 mg'
                }
            ),

            'frequency': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: Twice a day'
                }
            ),

            'duration': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: 5 days'
                }
            ),

            'instructions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Example: Take after food'
                }
            ),
        }

        labels = {
            'medicine_name': 'Medicine Name',
            'dosage': 'Dosage',
            'frequency': 'Frequency',
            'duration': 'Duration',
            'instructions': 'Medicine Instructions'
        }