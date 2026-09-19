from django.urls import path

from . import views


urlpatterns = [

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    # =====================================================
    # PATIENT PROFILE
    # =====================================================

    path(
        'patient/profile/',
        views.patient_profile,
        name='patient_profile'
    ),

    path(
        'patient/profile/edit/',
        views.edit_patient_profile,
        name='edit_patient_profile'
    ),

]