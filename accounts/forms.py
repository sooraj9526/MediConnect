from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class RegistrationForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number'
        })
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter address'
        })
    )


class PatientProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            'phone',
            'address',
            'profile_picture',
        ]

        widgets = {

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter address'
            }),

            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class PatientUserForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'email',
        ]

        widgets = {

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),

        }