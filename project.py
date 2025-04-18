import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
import csv

# --- Database Connection ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TanKum090705",  # <--- your mysql password
        database="clinic"
    )

# --- Login Window ---
def show_login():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT role FROM users WHERE username=%s AND password=%s", (username, password))
            result = cursor.fetchone()
            if result:
                role = result[0]
                login_window.destroy()
                show_dashboard(username, role)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    login_window = tk.Tk()
    login_window.title("Clinic Login")
    login_window.geometry("360x240")
    login_window.configure(bg="#e0e0e0")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Clinic Login", font=("Arial", 16, "bold"), bg="#e0e0e0", fg="#333").pack(pady=10)

    form_frame = tk.Frame(login_window, bg="#e0e0e0")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_username = tk.Entry(form_frame, font=("Arial", 11), width=25)
    entry_username.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Password:", bg="#e0e0e0", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_password = tk.Entry(form_frame, show="*", font=("Arial", 11), width=25)
    entry_password.grid(row=1, column=1, pady=5)

    tk.Button(login_window, text="Login", command=login, bg="#007acc", fg="white", font=("Arial", 11, "bold"), width=20).pack(pady=10)

    login_window.mainloop()
# --- Dashboard Window ---
def show_dashboard(username, role):
    db = connect_db()
    cursor = db.cursor()

    root = tk.Tk()
    root.title(f"{role.capitalize()} Dashboard - Logged in as {username}")
    root.geometry("1200x750")
    root.configure(bg="#e0e0e0")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_patient = tk.Frame(notebook, bg="#e0e0e0")
    tab_doctor = tk.Frame(notebook, bg="#e0e0e0")
    tab_nurse = tk.Frame(notebook, bg="#e0e0e0")
    tab_appointment = tk.Frame(notebook, bg="#e0e0e0")
    tab_prescription = tk.Frame(notebook, bg="#e0e0e0")

    notebook.add(tab_patient, text="Patients")
    notebook.add(tab_doctor, text="Doctors")
    notebook.add(tab_nurse, text="Nurses")
    notebook.add(tab_appointment, text="Appointments")
    notebook.add(tab_prescription, text="Prescriptions")

    def logout():
        root.destroy()
        show_login()
    # --- Universal Form Builder ---
    def create_form(tab, fields, table, special_type=None):
        entries = {}
        search_var = tk.StringVar()
        gender_var = tk.StringVar(value="All")

        search_frame = tk.Frame(tab, bg="#e0e0e0")
        search_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)

        if special_type == "appointments":
            tk.Label(search_frame, text="Search by Patient ID:", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=0, padx=5)
            tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=20).grid(row=0, column=1)
        elif special_type == "prescriptions":
            tk.Label(search_frame, text="Search by Appointment ID:", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=0, padx=5)
            tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=20).grid(row=0, column=1)
        else:
            tk.Label(search_frame, text="Search by Name:", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=0, padx=5)
            tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=20).grid(row=0, column=1)

        tk.Label(search_frame, text="Gender:", bg="#e0e0e0", font=("Arial", 11)).grid(row=0, column=2, padx=5)
        gender_combo = ttk.Combobox(search_frame, textvariable=gender_var, values=["All", "Male", "Female", "Other"], width=12)
        gender_combo.grid(row=0, column=3)
        gender_combo.current(0)

        def search():
            for row in tree.get_children():
                tree.delete(row)

            filters = []
            values = []

            if special_type == "appointments":
                query = """
                    SELECT a.appointment_id, a.patient_id, p.name, p.gender, a.doctor_id, a.date, a.time, a.reason
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                """
                if search_var.get().strip():
                    filters.append("a.patient_id = %s")
                    values.append(search_var.get().strip())
                if gender_var.get() != "All":
                    filters.append("p.gender = %s")
                    values.append(gender_var.get())
            elif special_type == "prescriptions":
                query = """
                    SELECT pr.prescription_id, pr.appointment_id, p.name, p.gender, pr.diagnosis, pr.treatment, pr.notes
                    FROM prescriptions pr
                    JOIN appointments a ON pr.appointment_id = a.appointment_id
                    JOIN patients p ON a.patient_id = p.patient_id
                """
                if search_var.get().strip():
                    filters.append("pr.appointment_id = %s")
                    values.append(search_var.get().strip())
                if gender_var.get() != "All":
                    filters.append("p.gender = %s")
                    values.append(gender_var.get())
            else:
                query = f"SELECT * FROM {table}"
                if search_var.get().strip():
                    filters.append("name LIKE %s")
                    values.append(f"%{search_var.get().strip()}%")
                if gender_var.get() != "All":
                    filters.append("gender = %s")
                    values.append(gender_var.get())

            if filters:
                query += " WHERE " + " AND ".join(filters)

            cursor.execute(query, tuple(values))
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

        tk.Button(search_frame, text="Search", command=search, bg="#2980b9", fg="white", font=("Arial", 11, "bold"), width=10).grid(row=0, column=4, padx=10)
        show_fields = (username == "admin1")
        form_row = 1

        if show_fields and special_type not in ["appointments", "prescriptions"]:
            for label, widget_type in fields:
                if widget_type == "readonly":
                    continue
                tk.Label(tab, text=label, bg="#e0e0e0", font=("Arial", 11)).grid(row=form_row, column=0, padx=10, pady=5, sticky="e")
                if widget_type == "entry":
                    e = tk.Entry(tab, font=("Arial", 11))
                elif widget_type == "date":
                    e = DateEntry(tab, date_pattern='yyyy-mm-dd')
                elif widget_type == "combo":
                    e = ttk.Combobox(tab, values=["Male", "Female", "Other"], font=("Arial", 11))
                    e.current(0)
                elif widget_type == "text":
                    e = tk.Text(tab, height=2, width=30, font=("Arial", 11))
                entries[label] = e
                e.grid(row=form_row, column=1, padx=10, pady=5, sticky="w")
                form_row += 1

        def clear():
            for widget in entries.values():
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                elif isinstance(widget, ttk.Combobox):
                    widget.set(widget["values"][0])

        def insert():
            if username != "admin1":
                messagebox.showwarning("Access Denied", "Only admin1 can add entries.")
                return
            values = [widget.get() if not isinstance(widget, tk.Text) else widget.get("1.0", tk.END).strip()
                      for widget in entries.values()]
            query = ""
            if table == "patients":
                query = "INSERT INTO patients (name, dob, gender, contact, address) VALUES (%s, %s, %s, %s, %s)"
            elif table == "doctors":
                query = "INSERT INTO doctors (name, specialization, phone) VALUES (%s, %s, %s)"
            elif table == "nurses":
                query = "INSERT INTO nurses (name, department, phone) VALUES (%s, %s, %s)"
            try:
                cursor.execute(query, tuple(values))
                db.commit()
                messagebox.showinfo("Success", f"{table[:-1].capitalize()} added.")
                load_data()
                clear()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", str(err))

        def delete():
            if username != "admin1":
                messagebox.showwarning("Access Denied", "Only admin1 can delete.")
                return
            selected_item = tree.selection()
            if selected_item:
                item_id = tree.item(selected_item)['values'][0]
                cursor.execute(f"DELETE FROM {table} WHERE id = %s", (item_id,))
                db.commit()
                load_data()

        def export_csv():
            if username != "admin1":
                messagebox.showwarning("Access Denied", "Only admin1 can export.")
                return
            rows = [tree.item(row)['values'] for row in tree.get_children()]
            if rows:
                file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if file:
                    with open(file, mode='w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([label for label, _ in fields])
                        writer.writerows(rows)
                    messagebox.showinfo("Exported", "Data exported successfully.")
            else:
                messagebox.showinfo("No Data", "Nothing to export.")
        if show_fields:
            row_offset = form_row + 1
            tk.Button(tab, text="Add", command=insert, bg="#007acc", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=row_offset, column=0, pady=10)
            tk.Button(tab, text="Clear", command=clear, font=("Arial", 11, "bold"), width=12).grid(row=row_offset, column=1, pady=10)
            tk.Button(tab, text="Export CSV", command=export_csv, bg="#16a085", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=row_offset + 1, column=0, pady=5)
            tk.Button(tab, text="Delete", command=delete, bg="tomato", fg="white", font=("Arial", 11, "bold"), width=12).grid(row=row_offset + 1, column=1, pady=5)
            tree_row = row_offset + 2
        else:
            tree_row = 2

        columns = [label for label, _ in fields]
        tree = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
        tree.grid(row=tree_row, column=0, columnspan=5, padx=10, pady=10)

        def load_data():
            for row in tree.get_children():
                tree.delete(row)

            if special_type == "appointments":
                query = """
                    SELECT a.appointment_id, a.patient_id, p.name, p.gender, a.doctor_id, a.date, a.time, a.reason
                    FROM appointments a
                    JOIN patients p ON a.patient_id = p.patient_id
                """
            elif special_type == "prescriptions":
                query = """
                    SELECT pr.prescription_id, pr.appointment_id, p.name, p.gender, pr.diagnosis, pr.treatment, pr.notes
                    FROM prescriptions pr
                    JOIN appointments a ON pr.appointment_id = a.appointment_id
                    JOIN patients p ON a.patient_id = p.patient_id
                """
            else:
                query = f"SELECT * FROM {table}"

            cursor.execute(query)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

        load_data()
    # --- Fields Setup ---
    patient_fields = [
        ("id", "readonly"),
        ("name", "entry"),
        ("dob", "date"),
        ("gender", "combo"),
        ("contact", "entry"),
        ("address", "text")
    ]

    doctor_fields = [
        ("id", "readonly"),
        ("name", "entry"),
        ("specialization", "entry"),
        ("phone", "entry")
    ]

    nurse_fields = [
        ("id", "readonly"),
        ("name", "entry"),
        ("department", "entry"),
        ("phone", "entry")
    ]

    appointment_fields = [
        ("appointment_id", "readonly"),
        ("patient_id", "readonly"),
        ("patient_name", "readonly"),
        ("gender", "readonly"),
        ("doctor_id", "readonly"),
        ("date", "readonly"),
        ("time", "readonly"),
        ("reason", "readonly")
    ]

    prescription_fields = [
        ("prescription_id", "readonly"),
        ("appointment_id", "readonly"),
        ("patient_name", "readonly"),
        ("gender", "readonly"),
        ("diagnosis", "readonly"),
        ("treatment", "readonly"),
        ("notes", "readonly")
    ]

    # --- Create Tabs ---
    create_form(tab_patient, patient_fields, "patients")
    create_form(tab_doctor, doctor_fields, "doctors")
    create_form(tab_nurse, nurse_fields, "nurses")
    create_form(tab_appointment, appointment_fields, "appointments", special_type="appointments")
    create_form(tab_prescription, prescription_fields, "prescriptions", special_type="prescriptions")

    # --- Logout Button and Footer ---
    tk.Button(root, text="Logout", command=logout, bg="red", fg="white", font=("Arial", 11, "bold"), width=10).pack(pady=10)
    tk.Label(root, text=f"Logged in as: {username} ({role})", font=("Arial", 10), bg="#e0e0e0").pack(fill="x")

    root.mainloop()
# --- Start App ---
show_login()