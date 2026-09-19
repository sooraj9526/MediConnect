"""
URL configuration for mediconnect project.

The `urlpatterns` list routes URLs to views.

For more information please see:
https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static


# =========================================================
# HOME
# =========================================================

def home(request):
    return redirect('login')


# =========================================================
# URL PATTERNS
# =========================================================

urlpatterns = [

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'admin/',
        admin.site.urls
    ),


    # =====================================================
    # HOME
    # =====================================================

    path(
        '',
        home,
        name='home'
    ),


    # =====================================================
    # ACCOUNTS
    # =====================================================

    path(
        '',
        include('accounts.urls')
    ),


    # =====================================================
    # APPOINTMENTS
    # =====================================================

    path(
        'appointments/',
        include('appointments.urls')
    ),

]


# =========================================================
# MEDIA FILES
# =========================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )