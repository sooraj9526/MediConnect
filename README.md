# MediConnect 🏥

## Django-Based Healthcare Management System

MediConnect is a Django-based healthcare management system designed to connect patients, doctors, laboratory technicians, and receptionists through a centralized web application.

The system provides role-based dashboards and helps manage appointments, laboratory tests, medical reports, and prescriptions.

---

## 📌 Project Overview

MediConnect provides different features for different healthcare users.

### 👤 Patient

Patients can:

- Register and log in
- View their dashboard
- Book appointments with doctors
- View their appointments
- Cancel appointments
- View laboratory reports
- Download laboratory reports
- View prescriptions

### 👨‍⚕️ Doctor

Doctors can:

- Log in to their dashboard
- View appointments
- View patient information
- Request laboratory tests
- Create prescriptions
- View prescription details

### 🧪 Laboratory Technician

Laboratory technicians can:

- View pending laboratory test requests
- Start laboratory tests
- Process tests
- Complete tests
- Upload laboratory reports
- View completed tests

### 🧑‍💼 Receptionist

Receptionists can:

- View patients
- View doctors
- View appointments
- Book appointments for patients
- Manage appointment-related information

---

# 🚀 Main Features

- 🔐 User registration and authentication
- 👥 Role-based access
- 📊 Role-based dashboards
- 📅 Doctor appointment booking
- ❌ Appointment cancellation
- 🧪 Laboratory test management
- 🔬 Laboratory test processing workflow
- 📄 Medical laboratory report upload
- ⬇️ Laboratory report download
- 💊 Prescription management
- 👨‍⚕️ Doctor-patient management
- 🧑‍💼 Receptionist management
- 🛡️ Login-protected healthcare modules
- 📁 Media file handling for laboratory reports

---

# 🧪 Laboratory Workflow

The laboratory module follows a complete workflow:

```text
Doctor
   │
   │ Request Laboratory Test
   ▼
Pending Test
   │
   │ Start Test
   ▼
Processing
   │
   │ Complete Test
   ▼
Completed
   │
   │ Upload Report
   ▼
Patient
   │
   │ View / Download Report
   ▼
Laboratory Report