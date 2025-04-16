# ClinicManagementSystem
# Clinic Management System

This is a desktop application using Python (Tkinter) and MySQL that allows role-based management of a clinic's patients, doctors, and nurses.

## Features
- Login with roles: admin1 / doctor / nurse
- Tabbed UI with role-restricted controls
- Admin-only: add, delete, export to CSV
- Search by name and gender
- Responsive UI and visual feedback

## Setup
1. Import schema.sql into MySQL
2. Update DB credentials in `project.py`
3. Run using `python project.py`

## Roles
| Username   | Password   | Role    |
|------------|------------|---------|
| admin1     | adminpass  | admin   |
| drjones    | docpass    | doctor  |
| nurseamy   | nursepass  | nurse   |
