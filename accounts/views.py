from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from appointments.models import Appointment, LabTest, LabReport

from .forms import (
    RegistrationForm,
    PatientProfileForm,
    PatientUserForm
)

from .models import UserProfile


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            login(request, user)

            return redirect('dashboard')

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        next_url = request.POST.get('next')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect('dashboard')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'accounts/login.html'
    )


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect('login')


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    profile = UserProfile.objects.get(
        user=request.user
    )


    # =====================================================
    # PATIENT DASHBOARD
    # =====================================================

    if profile.role == 'patient':

        return render(
            request,
            'accounts/patient_dashboard.html',
            {
                'profile': profile
            }
        )


    # =====================================================
    # DOCTOR DASHBOARD
    # =====================================================

    elif profile.role == 'doctor':

        return render(
            request,
            'accounts/doctor_dashboard.html',
            {
                'profile': profile
            }
        )


    # =====================================================
    # LAB TECHNICIAN DASHBOARD
    # =====================================================

    elif profile.role == 'lab_technician':

        # -------------------------------------------------
        # PENDING LABORATORY TESTS
        # -------------------------------------------------

        pending_tests = LabTest.objects.filter(
            status='pending'
        ).select_related(
            'patient',
            'requested_by'
        ).order_by(
            '-created_at'
        )


        # -------------------------------------------------
        # PENDING TEST COUNT
        # -------------------------------------------------

        pending_tests_count = pending_tests.count()


        # -------------------------------------------------
        # PROCESSING TEST COUNT
        # -------------------------------------------------

        processing_tests_count = LabTest.objects.filter(
            status='processing'
        ).count()


        # -------------------------------------------------
        # COMPLETED TEST COUNT
        # -------------------------------------------------

        completed_tests_count = LabTest.objects.filter(
            status='completed'
        ).count()


        # -------------------------------------------------
        # LAB REPORT COUNT
        # -------------------------------------------------

        reports_count = LabReport.objects.count()


        # -------------------------------------------------
        # LAB TECHNICIAN DASHBOARD
        # -------------------------------------------------

        return render(
            request,
            'accounts/lab_dashboard.html',
            {
                'profile': profile,

                'pending_tests': pending_tests,

                'pending_tests_count': pending_tests_count,

                'processing_tests_count': processing_tests_count,

                'completed_tests_count': completed_tests_count,

                'reports_count': reports_count,
            }
        )


    # =====================================================
    # RECEPTIONIST DASHBOARD
    # =====================================================

    elif profile.role == 'receptionist':

        # -------------------------------------------------
        # TODAY'S DATE
        # -------------------------------------------------

        today = timezone.localdate()


        # -------------------------------------------------
        # TOTAL REGISTERED PATIENTS
        # -------------------------------------------------

        patient_count = User.objects.filter(
            userprofile__role='patient'
        ).count()


        # -------------------------------------------------
        # TOTAL DOCTORS
        # -------------------------------------------------

        doctor_count = User.objects.filter(
            userprofile__role='doctor'
        ).count()


        # -------------------------------------------------
        # TODAY'S APPOINTMENTS
        # -------------------------------------------------

        today_appointments = Appointment.objects.filter(
            appointment_date=today
        ).select_related(
            'patient',
            'doctor'
        ).order_by(
            'appointment_time'
        )


        # -------------------------------------------------
        # TODAY'S APPOINTMENT COUNT
        # -------------------------------------------------

        today_appointments_count = today_appointments.count()


        # -------------------------------------------------
        # PENDING APPOINTMENTS
        # -------------------------------------------------

        pending_appointments_count = Appointment.objects.filter(
            status='pending'
        ).count()


        return render(
            request,
            'accounts/receptionist_dashboard.html',
            {
                'profile': profile,

                'patient_count': patient_count,

                'doctor_count': doctor_count,

                'today_appointments_count': today_appointments_count,

                'pending_appointments_count': pending_appointments_count,

                'today_appointments': today_appointments,
            }
        )


    # =====================================================
    # DEFAULT DASHBOARD
    # =====================================================

    return render(
        request,
        'accounts/dashboard.html',
        {
            'profile': profile
        }
    )


# =========================================================
# PATIENT PROFILE
# =========================================================

@login_required
def patient_profile(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    return render(
        request,
        'accounts/patient_profile.html',
        {
            'profile': profile
        }
    )


# =========================================================
# EDIT PATIENT PROFILE
# =========================================================

@login_required
def edit_patient_profile(request):

    profile = UserProfile.objects.get(
        user=request.user
    )


    if request.method == 'POST':

        profile_form = PatientProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        user_form = PatientUserForm(
            request.POST,
            instance=request.user
        )


        if profile_form.is_valid() and user_form.is_valid():

            profile_form.save()

            user_form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect(
                'patient_profile'
            )


    else:

        profile_form = PatientProfileForm(
            instance=profile
        )

        user_form = PatientUserForm(
            instance=request.user
        )


    return render(
        request,
        'accounts/edit_patient_profile.html',
        {
            'profile_form': profile_form,

            'user_form': user_form,

            'profile': profile
        }
    )