from student_functions import student_menu
from admin_functions import admin_menu

def main():
    while True:
        print("\n--- University System ---")
        print("(A) Admin")
        print("(S) Student")
        print("(X) Exit Program")
        
        choice = input("Enter your choice: ")
        
        if choice == 'A' or choice.lower() == 'a':
            # Basic password protection for admin area
            password = input("Enter admin password: ")
            if password == "admin123":
                admin_menu()
            else:
                print("Incorrect admin password.")
        elif choice == 'S' or choice.lower() == 's':
            student_menu()
        elif choice == 'X' or choice.lower() == 'x' or choice.lower() == 'break':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()