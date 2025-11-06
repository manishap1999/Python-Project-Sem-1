import tkinter as tk
from tkinter import messagebox
from student_functions import * # I mean it's only a 100 line program, surely you have something bigger than a Voodoo Graphics card
from data_manager import read_data

def student_menu():
    clear_window()
    tk.Label(root, text="Student Portal", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Login", command=student_login).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

def student_login():
    clear_window()
    tk.Label(root, text="Student Login", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)
    tk.Label(root, text="Password:").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    def attempt_login():
        email = email_entry.get()
        password = password_entry.get()
        student = login_student_gui(email, password)
        if student:
            show_student_dashboard(student)
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password")
    tk.Button(root, text="Login", command=attempt_login).pack(pady=5)
    tk.Button(root, text="Back", command=student_menu).pack(pady=5)

def login_student_gui(email, password):
    students = read_data()
    for student in students:
        if student['email'] == email and student['password'] == password:
            return student
    return None

def show_student_dashboard(student):
    def enrol_and_notify():
        subjects = student.get('subjects', [])
        if len(student['subjects']) < 4:
            enrol_subject(student)
            messagebox.showinfo("Enrolment","Subject enrolled successfully!\n\nCurrent Subjects:\n" +
                                "\n".join([f"{subj['name']} - Mark: {subj['mark']} ({subj['grade']})" for subj in student['subjects']]))

        else:
            messagebox.showwarning("Enrolment Failed", "You are already enrolled in the maximum of 4 subjects.")
            
    
    def show_subjects(student): # Fuck this, I'm directly grabbing the fucking data.
        subjects = student.get('subjects', [])
        if subjects:
            subject_info = "\n".join(
                [f"{subj['name']} - Mark: {subj['mark']} ({subj['grade']})" for subj in subjects]
            )
            messagebox.showinfo("Your Subjects", subject_info)
        else:
            messagebox.showinfo("Your Subjects", "You are not currently enrolled in any subjects.")

        
    clear_window()
    tk.Label(root, text=f"Welcome, {student['name']}", font=("Arial", 14)).pack(pady=10)
    
    tk.Button(root, text="Enrol in Subject", command=enrol_and_notify).pack(pady=5)
    tk.Button(root, text="Show Subjects", command=lambda: show_subjects(student)).pack(pady=5)
    tk.Button(root, text="Logout", command=student_menu).pack(pady=5)
    



def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# --- Main GUI Setup ---
root = tk.Tk()
root.title("University System")
root.geometry("800x600")
student_menu()
root.mainloop()