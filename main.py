import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@#ug4qwer%#Q",
    database="student_db"
)
cursor = conn.cursor()

# Main Functions
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()

    if name and age and grade:
        query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, grade))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        fetch_students()
        clear_fields()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

def fetch_students():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

def update_student():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        student_id = values[0]
        name = name_entry.get()
        age = age_entry.get()
        grade = grade_entry.get()

        query = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id=%s"
        cursor.execute(query, (name, age, grade, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully!")
        fetch_students()
        clear_fields()
    else:
        messagebox.showwarning("Selection Error", "Please select a record to update.")

def delete_student():
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        student_id = values[0]

        query = "DELETE FROM students WHERE id=%s"
        cursor.execute(query, (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student deleted successfully!")
        fetch_students()
        clear_fields()
    else:
        messagebox.showwarning("Selection Error", "Please select a record to delete.")

def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)

def load_selected(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        grade_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])
        age_entry.insert(0, values[2])
        grade_entry.insert(0, values[3])

# Tkinter GUI Setup
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("800x500")

# Configure grid weights for resizing
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Input Fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10, sticky='w')
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

tk.Label(root, text="Age").grid(row=1, column=0, padx=10, pady=10, sticky='w')
age_entry = tk.Entry(root)
age_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

tk.Label(root, text="Grade").grid(row=2, column=0, padx=10, pady=10, sticky='w')
grade_entry = tk.Entry(root)
grade_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=0, column=2, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Update Student", command=update_student).grid(row=1, column=2, padx=10, pady=5, sticky="ew")
tk.Button(root, text="Delete Student", command=delete_student).grid(row=2, column=2, padx=10, pady=5, sticky="ew")

# Treeview + Scrollbar
columns = ('ID', 'Name', 'Age', 'Grade')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")
scrollbar.grid(row=3, column=3, sticky='ns')

# Bind Selection
tree.bind('<<TreeviewSelect>>', load_selected)

fetch_students()  # Load data at startup

root.mainloop()

# Close Connection after GUI exits
conn.close()
