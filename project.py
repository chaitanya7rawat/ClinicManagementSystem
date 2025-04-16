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
        password="VCCcst2000!",
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
    login_window.geometry("350x200")
    login_window.configure(bg="#f0f8ff")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Clinic Login", font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#333").pack(pady=10)

    form_frame = tk.Frame(login_window, bg="#f0f8ff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_username = tk.Entry(form_frame, width=25)
    entry_username.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Password:", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_password = tk.Entry(form_frame, show="*", width=25)
    entry_password.grid(row=1, column=1, pady=5)

    tk.Button(login_window, text="Login", command=login, bg="#007acc", fg="white", width=20).pack(pady=10)

    login_window.mainloop()

# --- Dashboard Window ---
def show_dashboard(username, role):
    db = connect_db()
    cursor = db.cursor()

    root = tk.Tk()
    root.title(f"{role.capitalize()} Dashboard")
    root.geometry("1080x650")
    root.configure(bg="#ffffff")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_patient = tk.Frame(notebook, bg="#f0f8ff")
    tab_doctor = tk.Frame(notebook, bg="#f0f8ff")
    tab_nurse = tk.Frame(notebook, bg="#f0f8ff")

    notebook.add(tab_patient, text="Patients")
    notebook.add(tab_doctor, text="Doctors")
    notebook.add(tab_nurse, text="Nurses")

    def logout():
        root.destroy()
        show_login()

    # Removed redundant login_window definition
    pass  # No additional login window logic is needed here

# --- Dashboard ---
def show_dashboard(username, role):
    db = connect_db()
    cursor = db.cursor()

    root = tk.Tk()
    root.title(f"{role.capitalize()} Dashboard - Logged in as {username}")
    root.geometry("1100x620")
    root.configure(bg="#f7f9fb")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_patient = tk.Frame(notebook, bg="#f7f9fb")
    tab_doctor = tk.Frame(notebook, bg="#f7f9fb")
    tab_nurse = tk.Frame(notebook, bg="#f7f9fb")

    notebook.add(tab_patient, text="Patients")
    notebook.add(tab_doctor, text="Doctors")
    notebook.add(tab_nurse, text="Nurses")

    def logout():
        root.destroy()
        show_login()

    def create_form(tab, fields, table):
        entries = {}

        search_var = tk.StringVar()
        gender_var = tk.StringVar(value="All")

        search_frame = tk.Frame(tab, bg="#f7f9fb")
        search_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)

        tk.Label(search_frame, text="Search by Name:", bg="#f7f9fb").grid(row=0, column=0, padx=5)
        tk.Entry(search_frame, textvariable=search_var, width=20).grid(row=0, column=1)

        tk.Label(search_frame, text="Gender:", bg="#f7f9fb").grid(row=0, column=2, padx=5)
        gender_combo = ttk.Combobox(search_frame, textvariable=gender_var, values=["All", "Male", "Female", "Other"], width=12)
        gender_combo.grid(row=0, column=3)
        gender_combo.current(0)

        def search():
            name_filter = search_var.get().strip()
            gender_filter = gender_var.get()
            for row in tree.get_children():
                tree.delete(row)

            base_query = f"SELECT * FROM {table}"
            filters = []
            values = []

            if name_filter:
                filters.append("name LIKE %s")
                values.append(f"%{name_filter}%")
            if gender_filter != "All":
                filters.append("gender = %s")
                values.append(gender_filter)

            if filters:
                query = base_query + " WHERE " + " AND ".join(filters)
                cursor.execute(query, tuple(values))
            else:
                cursor.execute(base_query)

            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

        tk.Button(search_frame, text="Search", command=search, bg="#2980b9", fg="white", width=10).grid(row=0, column=4, padx=10)

        show_fields = (username == "admin1")
        form_row = 1

        if show_fields:
            for label, widget_type in fields:
                if widget_type == "readonly":
                    continue
                tk.Label(tab, text=label, bg="#f7f9fb").grid(row=form_row, column=0, padx=10, pady=5, sticky="e")
                if widget_type == "entry":
                    e = tk.Entry(tab)
                elif widget_type == "date":
                    e = DateEntry(tab, date_pattern='yyyy-mm-dd')
                elif widget_type == "combo":
                    e = ttk.Combobox(tab, values=["Male", "Female", "Other"])
                    e.current(0)
                elif widget_type == "text":
                    e = tk.Text(tab, height=2, width=30)
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
            tk.Button(tab, text="Add", command=insert, bg="#007acc", fg="white", width=12).grid(row=row_offset, column=0, pady=10)
            tk.Button(tab, text="Clear", command=clear, width=12).grid(row=row_offset, column=1, pady=10)
            tk.Button(tab, text="Export CSV", command=export_csv, bg="#16a085", fg="white", width=12).grid(row=row_offset + 1, column=0, pady=5)
            tk.Button(tab, text="Delete", command=delete, bg="tomato", fg="white", width=12).grid(row=row_offset + 1, column=1, pady=5)
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
            cursor.execute(f"SELECT * FROM {table}")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

        load_data()

    patient_fields = [
        ("Student ID", "readonly"),
        ("Name", "entry"),
        ("DOB", "date"),
        ("Gender", "combo"),
        ("Contact", "entry"),
        ("Address", "text")
    ]

    doctor_fields = [
        ("Doctor ID", "readonly"),
        ("Name", "entry"),
        ("Specialization", "entry"),
        ("Phone", "entry")
    ]

    nurse_fields = [
        ("Nurse ID", "readonly"),
        ("Name", "entry"),
        ("Department", "entry"),
        ("Phone", "entry")
    ]

    create_form(tab_patient, patient_fields, "patients")
    create_form(tab_doctor, doctor_fields, "doctors")
    create_form(tab_nurse, nurse_fields, "nurses")

    tk.Button(root, text="Logout", command=logout, bg="tomato", fg="white", width=10).pack(pady=10)
    tk.Label(root, text=f"Logged in as: {username} ({role})", font=("Helvetica", 10), bg="#f7f9fb").pack(fill="x")

    root.mainloop()

# --- Start App ---
show_login()
