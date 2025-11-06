import os
from data_manager import read_data, write_data, STUDENTS_FILE

def show_all_students():
    students = read_data()
    if not students:
        print("\n< Nothing to Display! >")
        return
    print("\n--- All Students ---")
    for student in students:
        print(f"  ID: {student['id']} ||| Name: {student['name']} ||| Email: {student['email']}")

def clear_database():
    confirm = input("Are you sure you want to clear the entire database? ((Y)es/(N)o): ").lower()
    if confirm == 'yes' or confirm == 'y':
        if os.path.exists(STUDENTS_FILE):
            os.remove(STUDENTS_FILE)
            print("\nStudent database has been cleared.")
        else:
            print("\nDatabase is already empty.")
    else:
        print("\nOperation cancelled.")

def group_by_grade():
    students = read_data()
    if not students:
        print("\n< Nothing to Display! >")
        return

    grade_groups = {
        'HD (85-100)': [],
        'D (75-84)': [],
        'C (65-74)': [],
        'P (50-64)': [],
        'F (0-49)': [],
        'Not Graded': []
    }

    for student in students:
        subjects = student.get('subjects', [])
        if len(subjects) < 4:
            grade_groups['Not Graded'].append({
                'name': student['name'],
                'id': student['id'],
                'subjects': subjects
            })
            continue

        for subject in subjects:
            mark = subject.get('mark')
            subject_name = subject.get('name', 'Unknown Subject')
            grade = subject.get('grade', 'N/A')

            if mark is None:
                continue

            entry = {
                'name': student['name'],
                'id': student['id'],
                'subject': subject_name,
                'mark': mark,
                'grade': grade
            }

            if 85 <= mark <= 100:
                grade_groups['HD (85-100)'].append(entry)
            elif 75 <= mark <= 84:
                grade_groups['D (75-84)'].append(entry)
            elif 65 <= mark <= 74:
                grade_groups['C (65-74)'].append(entry)
            elif 50 <= mark <= 64:
                grade_groups['P (50-64)'].append(entry)
            elif 0 <= mark < 50:
                grade_groups['F (0-49)'].append(entry)

    # Display results
    # I'm concerned with how this is supposed to work; not graded should mean something but...
    print("\n--- Students Grouped by Subject Grades ---")
    for group_name, entries in grade_groups.items():
        if entries:
            print(f"\n{group_name}:")
            for entry in entries:
                if group_name == 'Not Graded':
                    print(f"  - {entry['name']} (ID: {entry['id']}) has fewer than 4 subjects.")
                    for subj in entry['subjects']:
                        print(f"      - {subj['name']}: {subj.get('mark', 'N/A')} ({subj.get('grade', 'N/A')})") 
                        # For those who are as lazy as I. This one also shows the grade letter because they cannot be fully graded.
                else:
                    print(f"  - {entry['name']} (ID: {entry['id']}) - {entry['subject']}: {entry['mark']}")

def partition_pass_fail():
    students = read_data()
    if not students:
        print("\n< Nothing to Display! >")
        return

    passing_grade = 50
    passed = []
    failed = []

    for student in students:
        subjects = student.get('subjects', [])

        for subject in subjects:
            # UGH.
            mark = subject.get('mark')
            subject_name = subject.get('name', 'Unknown Subject')
            
            if mark is not None:
                entry = {
                    'name': student['name'],
                    'id': student['id'],
                    'subject': subject_name,
                    'mark': mark
                }

                if mark >= passing_grade:
                    passed.append(entry)
                else:
                    failed.append(entry)


    print("\n--- Pass/Fail Partition ---")
    print("\nPASSING Students:")
    if passed:
        for s in passed:
            print(f"  - {s['name']} (ID: {s['id']}) passed {s['subject']} with {s['mark']}")
    else:
        print("  None")

    print("\nFAILING Students:")
    if failed:
        for s in failed:
            print(f"  - {s['name']} (ID: {s['id']}) passed {s['subject']} with {s['mark']}")
    else:
        print("  None")
        # At least it works

def remove_student_by_id():
    students = read_data()
    if not students:
        print("\n< Nothing to Display! >")
        return
    
    print("\n--- All Students ---")
    for student in students:
        print(f"  ID: {student['id']} ||| Name: {student['name']} ||| Email: {student['email']}")
        
    print("\n----------------")

    student_id = input("Enter the ID of the student to remove: ")
    
    # Create a new list excluding the student to be removed
    updated_students = [student for student in students if student['id'] != student_id]
    
    if len(updated_students) < len(students):
        write_data(updated_students)
        print(f"\nStudent with ID '{student_id}' has been removed.")
    else:
        print(f"\nNo student found with ID '{student_id}'.")


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("(S) Show all students")
        print("(R) Remove a student by ID")
        print("(G) Group students by grade")
        print("(P) Partition students to PASS/FAIL")
        print("(C) Clear database")
        print("(X) Exit to main menu")
        
        choice = input("Enter your choice: ")

        if choice == 'S' or choice.lower() == 's':
            show_all_students()
        elif choice == 'R' or choice.lower() == 'r':
            remove_student_by_id()
        elif choice == 'G 'or choice.lower() == 'g':
            group_by_grade()
        elif choice == 'P' or choice.lower() == 'p':
            partition_pass_fail()
        elif choice == 'C' or choice.lower() == 'c':
            clear_database()
        elif choice == 'X' or choice.lower() == 'x':
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice, please try again.")