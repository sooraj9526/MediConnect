from django.urls import path

from . import views


app_name = 'appointments'


urlpatterns = [

    # =====================================================
    # PATIENT APPOINTMENTS
    # =====================================================

    path(
        'book/',
        views.book_appointment,
        name='book'
    ),

    path(
        'my/',
        views.my_appointments,
        name='my_appointments'
    ),

    path(
        'cancel/<int:appointment_id>/',
        views.cancel_appointment,
        name='cancel_appointment'
    ),


    # =====================================================
    # DOCTOR
    # =====================================================

    path(
        'doctor/',
        views.doctor_appointments,
        name='doctor_appointments'
    ),

    path(
        'doctor/update/<int:appointment_id>/',
        views.update_appointment_status,
        name='update_appointment_status'
    ),

    path(
        'doctor/patients/',
        views.doctor_patients,
        name='doctor_patients'
    ),

    path(
        'doctor/lab-tests/request/',
        views.request_lab_test,
        name='request_lab_test'
    ),


    # =====================================================
    # LAB TECHNICIAN
    # =====================================================

    path(
        'lab/test-requests/',
        views.test_requests,
        name='test_requests'
    ),

    path(
        'lab/process-tests/',
        views.process_tests,
        name='process_tests'
    ),

    path(
        'lab/start-test/<int:test_id>/',
        views.start_test,
        name='start_test'
    ),

    path(
        'lab/complete-test/<int:test_id>/',
        views.complete_test,
        name='complete_test'
    ),

    path(
        'lab/upload-reports/',
        views.upload_reports,
        name='upload_lab_report'
    ),

    path(
        'lab/completed-reports/',
        views.completed_reports,
        name='completed_reports'
    ),


    # =====================================================
    # PATIENT LAB REPORTS
    # =====================================================

    path(
        'patient/lab-reports/',
        views.patient_lab_reports,
        name='patient_lab_reports'
    ),


    # =====================================================
    # PRESCRIPTIONS
    # =====================================================

    path(
        'doctor/prescriptions/create/',
        views.create_prescription,
        name='create_prescription'
    ),

    path(
        'doctor/prescriptions/<int:prescription_id>/',
        views.prescription_detail,
        name='prescription_detail'
    ),

    path(
        'patient/prescriptions/',
        views.my_prescriptions,
        name='my_prescriptions'
    ),


    # =====================================================
    # RECEPTIONIST
    # =====================================================

    path(
        'receptionist/patients/',
        views.receptionist_patients,
        name='receptionist_patients'
    ),

    path(
        'receptionist/doctors/',
        views.receptionist_doctors,
        name='receptionist_doctors'
    ),

    path(
        'receptionist/book-appointment/',
        views.receptionist_book_appointment,
        name='receptionist_book_appointment'
    ),

    path(
        'receptionist/appointments/',
        views.receptionist_appointments,
        name='receptionist_appointments'
    ),

    path(
        'receptionist/appointments/confirm/<int:appointment_id>/',
        views.receptionist_confirm_appointment,
        name='receptionist_confirm_appointment'
    ),

    path(
        'receptionist/appointments/cancel/<int:appointment_id>/',
        views.receptionist_cancel_appointment,
        name='receptionist_cancel_appointment'
    ),

    path(
        'receptionist/appointments/edit/<int:appointment_id>/',
        views.receptionist_edit_appointment,
        name='receptionist_edit_appointment'
    ),
]