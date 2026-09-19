from functools import wraps

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Prefetch, Q

from .models import (
    Appointment,
    LabTest,
    LabReport,
    Prescription,
    PrescriptionMedicine
)

from .forms import (
    AppointmentForm,
    LabTestRequestForm
)


# =========================================================
# ROLE PROTECTION
# =========================================================

def roles_required(*allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):

            profile = getattr(
                request.user,
                'userprofile',
                None
            )

            if (
                profile is None
                or profile.role not in allowed_roles
            ):

                messages.error(
                    request,
                    'You do not have permission to access this page.'
                )

                return redirect('dashboard')

            return view_func(
                request,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


patient_required = roles_required('patient')

doctor_required = roles_required('doctor')

lab_technician_required = roles_required(
    'lab_technician'
)

receptionist_required = roles_required(
    'receptionist'
)

doctor_or_patient_required = roles_required(
    'doctor',
    'patient'
)


# =========================================================
# PATIENT - BOOK APPOINTMENT
# =========================================================

@patient_required
def book_appointment(request):

    if request.method == 'POST':

        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get(
            'appointment_date'
        )
        appointment_time = request.POST.get(
            'appointment_time'
        )
        reason = request.POST.get(
            'reason',
            ''
        ).strip()

        if not doctor_id:

            messages.error(
                request,
                'Please select a doctor.'
            )

            return redirect(
                'appointments:book'
            )

        if not appointment_date:

            messages.error(
                request,
                'Please select an appointment date.'
            )

            return redirect(
                'appointments:book'
            )

        if not appointment_time:

            messages.error(
                request,
                'Please select an appointment time.'
            )

            return redirect(
                'appointments:book'
            )

        if not reason:

            messages.error(
                request,
                'Please enter the reason for your appointment.'
            )

            return redirect(
                'appointments:book'
            )

        doctor = get_object_or_404(
            User,
            id=doctor_id,
            userprofile__role='doctor'
        )

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status='pending'
        )

        messages.success(
            request,
            'Your appointment has been booked successfully!'
        )

        return redirect(
            'appointments:my_appointments'
        )

    doctors = User.objects.filter(
        userprofile__role='doctor'
    ).distinct()

    return render(
        request,
        'appointments/book_appointment.html',
        {
            'doctors': doctors
        }
    )


# =========================================================
# PATIENT - MY APPOINTMENTS
# =========================================================

@patient_required
def my_appointments(request):

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'appointments/my_appointments.html',
        {
            'appointments': appointments
        }
    )


# =========================================================
# PATIENT - CANCEL APPOINTMENT
# =========================================================

@patient_required
def cancel_appointment(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )

    appointment.status = 'cancelled'

    appointment.save()

    messages.success(
        request,
        'Appointment cancelled successfully.'
    )

    return redirect(
        'appointments:my_appointments'
    )


# =========================================================
# DOCTOR - VIEW APPOINTMENTS
# =========================================================

@doctor_required
def doctor_appointments(request):

    appointments = Appointment.objects.filter(
        doctor=request.user
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'appointments/doctor_appointments.html',
        {
            'appointments': appointments
        }
    )


# =========================================================
# DOCTOR - MY PATIENTS
# =========================================================

@doctor_required
def doctor_patients(request):

    doctor_appointments_list = Appointment.objects.filter(
        doctor=request.user
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    patients = User.objects.filter(
        patient_appointments__doctor=request.user
    ).distinct().prefetch_related(
        Prefetch(
            'patient_appointments',
            queryset=doctor_appointments_list,
            to_attr='doctor_patient_appointments'
        )
    ).order_by(
        'username'
    )

    return render(
        request,
        'appointments/doctor_patients.html',
        {
            'patients': patients
        }
    )


# =========================================================
# DOCTOR - UPDATE APPOINTMENT STATUS
# =========================================================

@doctor_required
def update_appointment_status(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        doctor_notes = request.POST.get(
            'doctor_notes',
            ''
        )

        valid_statuses = dict(
            Appointment.STATUS_CHOICES
        )

        if status in valid_statuses:

            appointment.status = status

            appointment.doctor_notes = doctor_notes

            appointment.save()

            messages.success(
                request,
                'Appointment updated successfully.'
            )

    return redirect(
        'appointments:doctor_appointments'
    )


# =========================================================
# DOCTOR - REQUEST LABORATORY TEST
# =========================================================

@doctor_required
def request_lab_test(request):

    form = LabTestRequestForm(
        request.POST or None,
        doctor=request.user
    )

    if request.method == 'POST':

        if form.is_valid():

            lab_test = form.save(
                commit=False
            )

            lab_test.requested_by = request.user

            lab_test.status = 'pending'

            lab_test.save()

            messages.success(
                request,
                'Laboratory test request sent successfully.'
            )

            return redirect(
                'appointments:doctor_appointments'
            )

    return render(
        request,
        'appointments/request_lab_test.html',
        {
            'form': form
        }
    )


# =========================================================
# LAB TECHNICIAN - TEST REQUESTS
# =========================================================

@lab_technician_required
def test_requests(request):

    pending_tests = LabTest.objects.filter(
        status='pending'
    ).select_related(
        'patient',
        'requested_by'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'appointments/test_requests.html',
        {
            'pending_tests': pending_tests
        }
    )


# =========================================================
# LAB TECHNICIAN - PROCESS TESTS
# =========================================================

@lab_technician_required
def process_tests(request):

    processing_tests = LabTest.objects.filter(
        status='processing'
    ).select_related(
        'patient'
    ).order_by(
        '-updated_at'
    )

    pending_tests = LabTest.objects.filter(
        status='pending'
    ).select_related(
        'patient'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'appointments/process_tests.html',
        {
            'tests': processing_tests,
            'pending_tests': pending_tests
        }
    )


# =========================================================
# LAB TECHNICIAN - START TEST
# =========================================================

@lab_technician_required
def start_test(
    request,
    test_id
):

    test = get_object_or_404(
        LabTest,
        id=test_id,
        status='pending'
    )

    test.status = 'processing'

    test.save()

    messages.success(
        request,
        f'{test.test_name} has been started.'
    )

    return redirect(
        'appointments:process_tests'
    )


# =========================================================
# LAB TECHNICIAN - COMPLETE TEST
# =========================================================

@lab_technician_required
def complete_test(
    request,
    test_id
):

    test = get_object_or_404(
        LabTest,
        id=test_id,
        status='processing'
    )

    test.status = 'completed'

    test.save()

    messages.success(
        request,
        f'{test.test_name} has been completed.'
    )

    return redirect(
        'appointments:process_tests'
    )


# =========================================================
# LAB TECHNICIAN - UPLOAD LAB REPORT
# =========================================================

@lab_technician_required
def upload_reports(request):

    tests = LabTest.objects.filter(
        status='completed'
    ).select_related(
        'patient'
    ).order_by(
        '-updated_at'
    )

    if request.method == 'POST':

        test_id = request.POST.get(
            'lab_test'
        )

        result = request.POST.get(
            'result',
            ''
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()

        report_file = request.FILES.get(
            'report_file'
        )

        if not test_id:

            messages.error(
                request,
                'Please select a laboratory test.'
            )

            return redirect(
                'appointments:upload_lab_report'
            )

        try:

            test = LabTest.objects.select_related(
                'patient'
            ).get(
                id=test_id,
                status='completed'
            )

        except LabTest.DoesNotExist:

            messages.error(
                request,
                'The selected laboratory test does not exist or is not completed.'
            )

            return redirect(
                'appointments:upload_lab_report'
            )

        if not result:

            messages.error(
                request,
                'Please enter the test result.'
            )

            return redirect(
                'appointments:upload_lab_report'
            )

        test_date = test.test_date

        if test_date is None:

            test_date = timezone.now().date()

        LabReport.objects.create(
            patient=test.patient,
            uploaded_by=request.user,
            lab_test=test,
            test_name=test.test_name,
            test_date=test_date,
            result=result,
            notes=notes,
            report_file=report_file
        )

        messages.success(
            request,
            'Laboratory report uploaded successfully.'
        )

        return redirect(
            'appointments:completed_reports'
        )

    return render(
        request,
        'appointments/upload_reports.html',
        {
            'tests': tests
        }
    )


# =========================================================
# LAB TECHNICIAN - COMPLETED REPORTS
# =========================================================

@lab_technician_required
def completed_reports(request):

    reports = LabReport.objects.select_related(
        'patient',
        'uploaded_by',
        'lab_test'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'appointments/completed_reports.html',
        {
            'reports': reports
        }
    )


# =========================================================
# PATIENT - VIEW LAB REPORTS
# =========================================================

@patient_required
def patient_lab_reports(request):

    reports = LabReport.objects.filter(
        patient=request.user
    ).select_related(
        'uploaded_by',
        'lab_test'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'appointments/patient_lab_reports.html',
        {
            'reports': reports
        }
    )


# =========================================================
# DOCTOR - CREATE PRESCRIPTION
# =========================================================

@doctor_required
def create_prescription(request):

    patients = User.objects.filter(
        patient_appointments__doctor=request.user
    ).distinct().order_by(
        'username'
    )

    appointments = Appointment.objects.filter(
        doctor=request.user
    ).select_related(
        'patient'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        appointment_id = request.POST.get(
            'appointment'
        )

        diagnosis = request.POST.get(
            'diagnosis',
            ''
        ).strip()

        instructions = request.POST.get(
            'instructions',
            ''
        ).strip()

        if not patient_id:

            messages.error(
                request,
                'Please select a patient.'
            )

            return redirect(
                'appointments:create_prescription'
            )

        patient = get_object_or_404(
            User,
            id=patient_id
        )

        appointment = None

        if appointment_id:

            appointment = get_object_or_404(
                Appointment,
                id=appointment_id,
                doctor=request.user,
                patient=patient
            )

        prescription = Prescription.objects.create(
            patient=patient,
            doctor=request.user,
            appointment=appointment,
            diagnosis=diagnosis,
            instructions=instructions
        )

        medicine_names = request.POST.getlist(
            'medicine_name'
        )

        dosages = request.POST.getlist(
            'dosage'
        )

        frequencies = request.POST.getlist(
            'frequency'
        )

        durations = request.POST.getlist(
            'duration'
        )

        medicine_instructions = request.POST.getlist(
            'medicine_instructions'
        )

        for index, medicine_name in enumerate(
            medicine_names
        ):

            medicine_name = medicine_name.strip()

            if not medicine_name:
                continue

            dosage = (
                dosages[index].strip()
                if index < len(dosages)
                else ''
            )

            frequency = (
                frequencies[index].strip()
                if index < len(frequencies)
                else ''
            )

            duration = (
                durations[index].strip()
                if index < len(durations)
                else ''
            )

            medicine_instruction = (
                medicine_instructions[index].strip()
                if index < len(medicine_instructions)
                else ''
            )

            PrescriptionMedicine.objects.create(
                prescription=prescription,
                medicine_name=medicine_name,
                dosage=dosage,
                frequency=frequency,
                duration=duration,
                instructions=medicine_instruction
            )

        messages.success(
            request,
            'Prescription created successfully.'
        )

        return redirect(
            'appointments:prescription_detail',
            prescription_id=prescription.id
        )

    return render(
        request,
        'appointments/create_prescription.html',
        {
            'patients': patients,
            'appointments': appointments
        }
    )


# =========================================================
# DOCTOR/PATIENT - VIEW PRESCRIPTION
# =========================================================

@doctor_or_patient_required
def prescription_detail(
    request,
    prescription_id
):

    prescription = get_object_or_404(
        Prescription.objects.select_related(
            'patient',
            'doctor',
            'appointment'
        ).prefetch_related(
            'medicines'
        ),
        id=prescription_id
    )

    if (
        prescription.doctor != request.user
        and prescription.patient != request.user
    ):

        messages.error(
            request,
            'You do not have permission to view this prescription.'
        )

        return redirect(
            'dashboard'
        )

    return render(
        request,
        'appointments/prescription_detail.html',
        {
            'prescription': prescription
        }
    )


# =========================================================
# PATIENT - MY PRESCRIPTIONS
# =========================================================

@patient_required
def my_prescriptions(request):

    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related(
        'doctor',
        'appointment'
    ).prefetch_related(
        'medicines'
    ).order_by(
        '-prescription_date',
        '-created_at'
    )

    return render(
        request,
        'appointments/my_prescriptions.html',
        {
            'prescriptions': prescriptions
        }
    )


# =========================================================
# RECEPTIONIST - VIEW ALL PATIENTS
# =========================================================

@receptionist_required
def receptionist_patients(request):

    search = request.GET.get(
        'q',
        ''
    ).strip()

    patients = User.objects.filter(
        userprofile__role='patient'
    ).select_related(
        'userprofile'
    )

    if search:

        patients = patients.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(userprofile__phone__icontains=search)
        )

    patients = patients.order_by(
        'username'
    )

    return render(
        request,
        'appointments/receptionist_patients.html',
        {
            'patients': patients,
            'search': search
        }
    )


# =========================================================
# RECEPTIONIST - VIEW ALL DOCTORS
# =========================================================

@receptionist_required
def receptionist_doctors(request):

    search = request.GET.get(
        'q',
        ''
    ).strip()

    doctors = User.objects.filter(
        userprofile__role='doctor'
    ).select_related(
        'userprofile'
    )

    if search:

        doctors = doctors.filter(
            Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(userprofile__phone__icontains=search)
            | Q(userprofile__address__icontains=search)
        )

    doctors = doctors.order_by(
        'username'
    )

    return render(
        request,
        'appointments/receptionist_doctors.html',
        {
            'doctors': doctors,
            'search': search
        }
    )


# =========================================================
# RECEPTIONIST - BOOK APPOINTMENT
# =========================================================

@receptionist_required
def receptionist_book_appointment(request):

    patients = User.objects.filter(
        userprofile__role='patient'
    ).select_related(
        'userprofile'
    ).order_by(
        'username'
    )

    doctors = User.objects.filter(
        userprofile__role='doctor'
    ).select_related(
        'userprofile'
    ).order_by(
        'username'
    )

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        doctor_id = request.POST.get(
            'doctor'
        )

        appointment_date = request.POST.get(
            'appointment_date'
        )

        appointment_time = request.POST.get(
            'appointment_time'
        )

        reason = request.POST.get(
            'reason',
            ''
        ).strip()

        if not patient_id:

            messages.error(
                request,
                'Please select a patient.'
            )

            return redirect(
                'appointments:receptionist_book_appointment'
            )

        if not doctor_id:

            messages.error(
                request,
                'Please select a doctor.'
            )

            return redirect(
                'appointments:receptionist_book_appointment'
            )

        if not appointment_date:

            messages.error(
                request,
                'Please select an appointment date.'
            )

            return redirect(
                'appointments:receptionist_book_appointment'
            )

        if not appointment_time:

            messages.error(
                request,
                'Please select an appointment time.'
            )

            return redirect(
                'appointments:receptionist_book_appointment'
            )

        if not reason:

            messages.error(
                request,
                'Please enter the reason for the appointment.'
            )

            return redirect(
                'appointments:receptionist_book_appointment'
            )

        patient = get_object_or_404(
            User,
            id=patient_id,
            userprofile__role='patient'
        )

        doctor = get_object_or_404(
            User,
            id=doctor_id,
            userprofile__role='doctor'
        )

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason,
            status='pending'
        )

        messages.success(
            request,
            f'Appointment booked successfully for {patient.username}.'
        )

        return redirect(
            'appointments:receptionist_appointments'
        )

    return render(
        request,
        'appointments/receptionist_book_appointment.html',
        {
            'patients': patients,
            'doctors': doctors
        }
    )


# =========================================================
# RECEPTIONIST - VIEW ALL APPOINTMENTS
# =========================================================

@receptionist_required
def receptionist_appointments(request):

    appointments = Appointment.objects.select_related(
        'patient',
        'doctor'
    ).order_by(
        '-appointment_date',
        '-appointment_time'
    )

    return render(
        request,
        'appointments/receptionist_appointments.html',
        {
            'appointments': appointments
        }
    )


# =========================================================
# RECEPTIONIST - CONFIRM APPOINTMENT
# =========================================================

@receptionist_required
def receptionist_confirm_appointment(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = 'confirmed'

    appointment.save()

    messages.success(
        request,
        'Appointment confirmed successfully.'
    )

    return redirect(
        'appointments:receptionist_appointments'
    )


# =========================================================
# RECEPTIONIST - CANCEL APPOINTMENT
# =========================================================

@receptionist_required
def receptionist_cancel_appointment(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    appointment.status = 'cancelled'

    appointment.save()

    messages.success(
        request,
        'Appointment cancelled successfully.'
    )

    return redirect(
        'appointments:receptionist_appointments'
    )


# =========================================================
# RECEPTIONIST - EDIT APPOINTMENT
# =========================================================

@receptionist_required
def receptionist_edit_appointment(
    request,
    appointment_id
):

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    patients = User.objects.filter(
        userprofile__role='patient'
    ).order_by(
        'username'
    )

    doctors = User.objects.filter(
        userprofile__role='doctor'
    ).order_by(
        'username'
    )

    if request.method == 'POST':

        patient_id = request.POST.get(
            'patient'
        )

        doctor_id = request.POST.get(
            'doctor'
        )

        appointment_date = request.POST.get(
            'appointment_date'
        )

        appointment_time = request.POST.get(
            'appointment_time'
        )

        reason = request.POST.get(
            'reason',
            ''
        ).strip()

        patient = get_object_or_404(
            User,
            id=patient_id,
            userprofile__role='patient'
        )

        doctor = get_object_or_404(
            User,
            id=doctor_id,
            userprofile__role='doctor'
        )

        appointment.patient = patient

        appointment.doctor = doctor

        appointment.appointment_date = appointment_date

        appointment.appointment_time = appointment_time

        appointment.reason = reason

        appointment.save()

        messages.success(
            request,
            'Appointment updated successfully.'
        )

        return redirect(
            'appointments:receptionist_appointments'
        )

    return render(
        request,
        'appointments/receptionist_book_appointment.html',
        {
            'appointment': appointment,
            'patients': patients,
            'doctors': doctors,
            'edit_mode': True
        }
    )