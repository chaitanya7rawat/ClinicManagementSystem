# 🏥 Clinic Management System

A role-based desktop application built with **Python (Tkinter)** and **MySQL** that streamlines the management of patients, doctors, nurses, appointments, and prescriptions in a clinic setting.

## Features

-  Role-based Login System (Admin, Doctor, Nurse)
-  Tabbed Interface for managing:
  - Patients
  - Doctors
  - Nurses
  - Appointments
  - Prescriptions
-  Search by Name and Gender or by ID (for appointments/prescriptions)
-  Read-Only and Editable Fields based on role
-  Admin-Only CSV Export and record management (Add/Delete)
-  Data Entry Forms with date pickers, dropdowns, and validation
-  Clean and responsive Tkinter UI

##  Tech Stack

- Frontend: Python Tkinter, Ttk, Tkcalendar
- Backend: MySQL (with `mysql-connector-python`)
- Database: Predefined schema (`clinic` database with required tables)

##  Default Roles & Credentials

| Role   | Username | Password   |
|--------|----------|------------|
| Admin  | admin1   | adminpass  |
| Doctor | drjones  | docpass    |
| Nurse  | nurseamy | nursepass  |

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ClinicManagementSystem.git
cd ClinicManagementSystem
