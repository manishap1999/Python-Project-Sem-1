import re
import random
import uuid
from data_manager import read_data, write_data

# --- Validation Patterns ---
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
# Password requires these conditions three: (i) It starts with an upper-case character, (ii) It contains at least five (5) letters, (iii) It is followed by three (3) or more digits.
PASSWORD_PATTERN = r'^[A-Z][A-Za-z]{4,}[0-9]{3,}$'

#Resigstration
def register_student():
    print("\n--- Student Registration ---")
    students = read_data()

    # Email
    while True:
        email = input("Enter email: ")
        if re.match(EMAIL_PATTERN, email):
            if any(student['email'] == email for student in students):
                print("This email is already registered!.")
            else:
                break
        else:
            print("Invalid email format. Use this format! user@example.com")

    # Password
    while True:
        password = input("Enter password (Start with Uppercase, have at least 5 letters, then follow it up with 3 numbers): ")
        if re.match(PASSWORD_PATTERN, password):
            break
        else:
            print("Password does not meet requirements. Please try again.")

    name = input("Enter your full name: ")

    # Create and Save new students
    new_student = {
        "id": f"{(uuid.uuid4().int % 999999) + 1:06d}", # Generate UUID, convert to integer, then modulo to get 0 to 999998, then add 1. Also format to a six digit with zeroes appended at the front.
        "name": name,
        "email": email,
        "password": password, 
        "subjects": []
    }
    students.append(new_student)
    write_data(students)
    print(f"\nRegistration successful! Welcome, {name}. Your student ID is {new_student['id']}.")

#Logging In
def login_student():
    print("\n--- Student Login ---")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    students = read_data()
    for student in students:
        if student['email'] == email and student['password'] == password:
            print(f"\nLogin successful. Welcome back, {student['name']}!") 
            return student

    print("\nError: Incorrect email or password.")
    return None

#Change Password
def change_password(logged_in_student):
    print("\n--- Change Password ---")
    current_password = input("Enter your current password: ")

    if current_password != logged_in_student['password']:
        print("Incorrect current password. Action cancelled.")
        return

    while True:
        new_password = input("Enter new password (Start with Uppercase, have at least 5 letters, then follow it up with 3 numbers): ")
        
        if new_password == logged_in_student['password']:
            print("New password cannot be the same as your current password. Please try again.")
            continue
        
        if re.match(PASSWORD_PATTERN, new_password):
            students = read_data()
            for student in students:
                if student['id'] == logged_in_student['id']:
                    student['password'] = new_password
                    break
            write_data(students)
            logged_in_student['password'] = new_password
            print("Password changed successfully.")
            break
        else:
            print("New password does not meet requirements. Please try again.")

#Enroll in Subject
def enrol_subject(student):
    print("\n--- Auto-Enrol in a Subject ---")
    # Check if student has already enrolled in 4 subjects
    if len(student['subjects']) >= 4:
        print("You are already enrolled in the maximum of 4 subjects.")
        return

    # Generate a random subject number
    subject_number = f"{random.randint(1, 999):03}"
    subject_name = f"Subject-{subject_number}"

    # Generate a random mark between 25 and 100
    mark = random.randint(25, 100)

    # Determine grade based on mark
    if mark >= 85:
        grade = 'HD'
    elif mark >= 75:
        grade = 'D'
    elif mark >= 65:
        grade = 'C'
    elif mark >= 50:
        grade = 'P'
    else:
        grade = 'F'

    # Add subject with mark and grade to student record
    student['subjects'].append({
        'name': subject_name,
        'mark': mark,
        'grade': grade
    })

    # Update the master students list
    students = read_data()
    for s in students:
        if s['id'] == student['id']:
            s['subjects'] = student['subjects']
            break
    write_data(students)

    print(f"Successfully enrolled in {subject_name} with mark {mark} ({grade}).")

    if len(student['subjects']) <= 4:
        print("You are now enrolled in " + str(len(student['subjects'])) + " of 4 subjects.")
        return
    # This if condition is probably (absolutely) unnessary but I legit do not give a damn

#Reomve a Subject
def remove_subject(student):
    print("\n--- Remove a Subject ---")
    enrolled = student['subjects']

    if not enrolled:
        print("You are not enrolled in any subjects.")
        return

    print("Your enrolled subjects:")
    # Enumerate all the subjects so that students can see what they are enrolled in
    for i, subject in enumerate(enrolled, 1):
        print(f"{i}. {subject['name']} - Mark: {subject['mark']} ({subject['grade']})")

    subject_id = input("Enter the 3-digit subject ID to remove (e.g., 123 for Subject-123): ").strip()
    subject_to_remove = None

    for subject in enrolled:
        if subject['name'].endswith(subject_id):
            subject_to_remove = subject
            break

    if subject_to_remove:
        enrolled.remove(subject_to_remove)

        # Update the master students list
        students = read_data()
        for s in students:
            if s['id'] == student['id']:
                s['subjects'] = enrolled
                break
        write_data(students)

        print(f"Successfully removed {subject_to_remove['name']}.")
    else:
        print("No subject found with that ID.")

#Show Subjects
def show_subjects(student):
    print("\n--- Your Enrolled Subjects ---")
    if student['subjects']:
        for subject in student['subjects']:
            print(f"- {subject}")
    else:
        print("You are not currently enrolled in any subjects.")

#Menu
def logged_in_menu(student):
    while True:
        print(f"\n--- Welcome, {student['name']}! ---")
        print("(C) Change password")
        print("(E) Enrol into a subject")
        print("(R) Remove a subject")
        print("(S) Show my subjects")
        print("(X) Logout")

        choice = input("Enter your choice: ")

        if choice == 'C' or choice.lower() == 'c':
            change_password(student)
        elif choice == 'E' or choice.lower() == 'e':
            enrol_subject(student)
        elif choice == 'R' or choice.lower() == 'r':
            remove_subject(student)
        elif choice == 'S' or choice.lower() == 's':
            show_subjects(student)
        elif choice == 'X' or choice.lower() == 'x':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

#student Menu
def student_menu():
    while True:
        print("\n--- Student Portal ---")
        print("(L) Login")
        print("(R) Register")
        print("(X) Exit to main menu")

        choice = input("Enter your choice: ")

        if choice == 'L' or choice.lower() == 'l':
            logged_in_student = login_student()
            if logged_in_student:
                logged_in_menu(logged_in_student)
        elif choice == 'R' or choice.lower() == 'r':
            register_student()
        elif choice == 'X' or choice.lower() == 'x':
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice, please try again.")